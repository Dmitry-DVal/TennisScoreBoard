import logging
from typing import Tuple, Any
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm import aliased

from tennis_app.database import session
from tennis_app.models import MatchesOrm, PlayerOrm
from tennis_app.services import Match

logger = logging.getLogger("app_logger")


class MatchDAO:
    @staticmethod
    def create_match(id_first_player: int, id_second_player: int) -> MatchesOrm:
        with session() as db_session:
            match_uuid = str(uuid4())
            match = MatchesOrm(
                UUID=match_uuid, Player1=id_first_player,
                Player2=id_second_player,
                Score={"sets": [0, 0], "games": [0, 0], "points": [0, 0]}
            )

            db_session.add(match)
            db_session.commit()
            db_session.refresh(match)
        return match

    @staticmethod
    def get_match_by_uuid(match_id: str) -> MatchesOrm | None:
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            return match  # Явно возвращаем match, даже если None

    def update_match_score(self, match_id: str, player: str) -> MatchesOrm | None:
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            if not match:
                return None

            match_obj = Match.from_dict(match.Score)

            match_obj.set_obj.game_obj.add_point(player)

            self.check_match_completion(match_id, player, match_obj)

            return match

    def check_match_completion(self, match_id: str, player: str, match_obj) -> None:
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            if match_obj.state.is_match_over:
                winner_id = match.Player1 if player == 0 else match.Player2
                db_session.query(MatchesOrm).filter_by(UUID=match_id).update(
                    {"Score": match_obj.to_dict(), "Winner": winner_id}
                )
            else:
                db_session.query(MatchesOrm).filter_by(UUID=match_id).update(
                    {"Score": match_obj.to_dict()}
                )
            db_session.commit()

    def build_match_query(self, db_session: Session,
                          player_name: str | None = None) -> Query:
        """Формирует базовый SQL-запрос для поиска завершённых матчей."""
        player1 = aliased(PlayerOrm)
        player2 = aliased(PlayerOrm)
        winner = aliased(PlayerOrm)

        query = db_session.query(
            player1.Name.label("player1"),
            player2.Name.label("player2"),
            winner.Name.label("winner"),
            MatchesOrm.Score["sets"].label("score_sets")
        ).join(player1, MatchesOrm.Player1 == player1.ID
               ).join(player2, MatchesOrm.Player2 == player2.ID
                      ).join(winner, MatchesOrm.Winner == winner.ID
                             ).filter(MatchesOrm.Winner.isnot(None))

        if player_name:
            player_name = f"%{player_name.lower()}%"
            query = query.filter(
                (func.lower(player1.Name).like(player_name)) |
                (func.lower(player2.Name).like(player_name))
            )

        return query

    def paginate_query(self, query: Query, page: int, per_page: int) \
            -> Tuple[list[Any], int]:
        total_matches = query.count()
        total_pages = max(1, -(-total_matches // per_page))
        matches = query.limit(per_page).offset((page - 1) * per_page).all()
        return matches, total_pages

    def get_completed_matches(self, player_name=None, page=1, per_page=5):
        with session() as db_session:
            query = self.build_match_query(db_session, player_name)
            return self.paginate_query(query, page, per_page)
