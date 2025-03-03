import logging
from uuid import uuid4

from sqlalchemy.orm import aliased

from src.database import session
from src.models.match_model import MatchesOrm
from src.models.player_model import PlayerOrm
from src.services.scoring_service import Match

logger = logging.getLogger("app_logger")


class MatchService:
    def create_match(self, id_first_player: int, id_second_player: int) -> MatchesOrm:
        """Создает матч"""
        with session() as db_session:
            match_uuid = str(uuid4())
            match = MatchesOrm(
                UUID=match_uuid, Player1=id_first_player,
                Player2=id_second_player,
                Score={"sets": [0, 0], "games": [0, 0], "points": [0, 0]}
            )

            db_session.add(match)
            db_session.commit()
            db_session.refresh(match)  # Обновляем объект, чтобы он не был "detached"
        return match

    def get_match_by_uuid(self, match_id: str) -> MatchesOrm | None:
        """Извлекает матч из БД по UUID и преобразует `Score` в словарь"""
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

    def check_match_completion(self, match_id: str, player: str, match_obj):
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            if match_obj.state.is_match_over:
                winner_id = match.Player1 if player == 0 else match.Player2  # Находим реальный ID игрока
                db_session.query(MatchesOrm).filter_by(UUID=match_id).update(
                    {"Score": match_obj.to_dict(), "Winner": winner_id}
                )
            else:
                db_session.query(MatchesOrm).filter_by(UUID=match_id).update(
                    {"Score": match_obj.to_dict()}
                )
            db_session.commit()

    def get_completed_matches(self):
        """Получает все завершенные матчи."""
        with (session() as db_session):
            Player1 = aliased(PlayerOrm)
            Player2 = aliased(PlayerOrm)
            Winner = aliased(PlayerOrm)

            matches = db_session.query(
                Player1.Name,
                Player2.Name,
                Winner.Name,
                MatchesOrm.Score['sets']).join(
                Player1, MatchesOrm.Player1 == Player1.ID).join(
                Player2, MatchesOrm.Player2 == Player2.ID).join(
                Winner, MatchesOrm.Winner == Winner.ID).filter(
                MatchesOrm.Winner.isnot(None)).all()
            logger.debug(type(matches))
            print()
            print(matches[0],
                  type(matches[0]))  # ...  <class 'sqlalchemy.engine.row.Row'>
            print()
            print(matches[0][0])  # Zhirna Mraz
            print(matches[0][1])  # Dima
            print(matches[0][2])  # Dima
            print(matches[0][3])  # [1, 2]
            print(len(matches))

            return matches
