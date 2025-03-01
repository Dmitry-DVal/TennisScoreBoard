import json
from uuid import uuid4

from src.database import session
from src.models.match_model import MatchesOrm
from src.services.scoring_service import Match

import logging
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
            if match and isinstance(match.Score,
                                    str):
                match.Score = json.loads(
                    match.Score)
            return match  # Явно возвращаем match, даже если None

    def update_match_score(self, match_id: str, player: str) -> MatchesOrm | None:
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            if not match:
                return None

            player = int(player)

            match_score = json.loads(match.Score) if isinstance(match.Score,
                                                                str) else match.Score
            match_obj = Match.from_dict(match_score)

            if match_obj.state.is_match_over:
                return match  # Возвращаем завершённый матч без изменений

            match_obj.set_obj.game_obj.add_point(player)

            # Если матч завершён, обновляем БД
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
            return match