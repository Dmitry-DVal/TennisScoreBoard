from typing import Any, Callable
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from sqlalchemy.sql.selectable import Select

from tennis_app.core.match_engine import Match
from tennis_app.models import MatchesOrm, PlayerOrm


class MatchDAO:
    def __init__(self, session: Callable[[], Session]):
        self.session = session

    def create_match(self, id_first_player: int, id_second_player: int) -> MatchesOrm:
        with self.session() as db_session:
            match_uuid = str(uuid4())
            match = MatchesOrm(
                UUID=match_uuid,
                Player1=id_first_player,
                Player2=id_second_player,
                Score={"sets": [0, 0], "games": [0, 0], "points": [0, 0]},
            )

            db_session.add(match)
            db_session.commit()
            db_session.refresh(match)
        return match

    def get_match_by_uuid(self, match_id: str) -> MatchesOrm | None:
        with self.session() as db_session:
            match = db_session.scalars(
                select(MatchesOrm).where(MatchesOrm.UUID == match_id)
            ).first()
            return match

    def update_match_score(self, match_id: str, player: int) -> MatchesOrm | None:
        with self.session() as db_session:
            match = db_session.scalars(
                select(MatchesOrm).where(MatchesOrm.UUID == match_id)
            ).first()
            if not match:
                return None

            match_obj = Match.from_dict(match.Score)

            match_obj.set_obj.game_obj.add_point(player)

            self.check_match_completion(match_id, player, match_obj)

            return match

    def check_match_completion(
        self, match_id: str, player: int, match_obj: Match
    ) -> None:
        with self.session() as db_session:
            match = db_session.scalars(
                select(MatchesOrm).where(MatchesOrm.UUID == match_id)
            ).first()
            if not match:
                return
            if match_obj.state.is_match_over:
                winner_id = match.Player1 if player == 0 else match.Player2
                db_session.execute(
                    update(MatchesOrm)
                    .where(MatchesOrm.UUID == match_id)
                    .values(Score=match_obj.to_dict(), Winner=winner_id)
                )

            else:
                db_session.execute(
                    update(MatchesOrm)
                    .where(MatchesOrm.UUID == match_id)
                    .values(Score=match_obj.to_dict())
                )

            db_session.commit()

    def build_match_query(self, player_name: str | None = None) -> Select:
        """Forms a basic SQL query to search for completed matches."""

        player1 = aliased(PlayerOrm)
        player2 = aliased(PlayerOrm)
        winner = aliased(PlayerOrm)

        stmt = (
            select(
                player1.Name.label("player1"),
                player2.Name.label("player2"),
                winner.Name.label("winner"),
                MatchesOrm.Score["sets"].label("score_sets"),
            )
            .join(player1, MatchesOrm.Player1 == player1.ID)
            .join(player2, MatchesOrm.Player2 == player2.ID)
            .join(winner, MatchesOrm.Winner == winner.ID)
            .where(MatchesOrm.Winner.is_not(None))
        )

        if player_name:
            name_like = f"%{player_name.lower()}%"
            stmt = stmt.where(
                func.lower(player1.Name).like(name_like)
                | func.lower(player2.Name).like(name_like)
            )

        return stmt

    def paginate_query(
        self, db_session: Session, stmt: Select, page: int, per_page: int
    ) -> tuple[list[Any], int]:
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_matches = db_session.scalar(count_stmt)
        if total_matches is None:
            total_matches = 0
        # total_matches = db_session.scalar(count_stmt)
        total_pages = max(1, -(-total_matches // per_page))

        paginated_stmt = stmt.limit(per_page).offset((page - 1) * per_page)
        # results = db_session.execute(paginated_stmt).all()
        results = list(db_session.execute(paginated_stmt).all())
        return results, total_pages

    # def get_completed_matches(self, player_name=None, page: int = 1,
    #                           per_page: int = 5) -> tuple[list[Any], int]:
    def get_completed_matches(
        self,
        player_name: str | None = None,
        page: int = 1,
        per_page: int = 5,
    ) -> tuple[list[Any], int]:
        with self.session() as db_session:
            stmt = self.build_match_query(player_name)
            return self.paginate_query(db_session, stmt, page, per_page)
