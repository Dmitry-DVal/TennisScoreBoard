from uuid import uuid4

from src.database import session
from src.models.match_model import MatchesOrm


class MatchService:
    def create_match(self, id_first_player: int, id_second_player: int) -> MatchesOrm:
        with session() as db_session:
            match_uuid = str(uuid4())
            match = MatchesOrm(UUID=match_uuid, Player1=id_first_player,
                               Player2=id_second_player, Score="{}")
            db_session.add(match)
            db_session.commit()
            db_session.refresh(match)  # Обновляем объект, чтобы он не был "detached"
        return match
