from src.database import session
from src.models.player_model import PlayerOrm


class PlayerDAO:
    def get_or_create_player(self, player_name: str) -> PlayerOrm:
        with session() as db_session:
            player = db_session.query(PlayerOrm).filter_by(Name=player_name).first()
            if not player:
                player = PlayerOrm(Name=player_name)
                db_session.add(player)
                db_session.commit()
                db_session.refresh(player)
            return player

    def get_players_name_by_id(self, player1_id: int, player2_id: int) -> list[str]:
        """Получает имя игрока по его ID"""
        with session() as db_session:
            player1_name = db_session.query(PlayerOrm).filter_by(ID=player1_id).first()
            player2_name = db_session.query(PlayerOrm).filter_by(ID=player2_id).first()
            return [player1_name.Name,
                    player2_name.Name] if player1_name and player2_name else "Unknown"
