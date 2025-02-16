from src.database import session
from src.models.player_model import PlayerOrm


class PlayerService:
    def get_or_create_player(self, player_name: str) -> PlayerOrm:
        with session() as db_session:  # Открываем новую сессию
            player = db_session.query(PlayerOrm).filter_by(Name=player_name).first()
            if not player:
                player = PlayerOrm(Name=player_name)
                db_session.add(player)
                db_session.commit()
                db_session.refresh(player)  # Обновляем объект из БД
            return player
