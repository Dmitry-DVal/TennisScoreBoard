from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from tennis_app.handlers.base_handler import logger
from tennis_app.models.player_model import PlayerOrm


class PlayerDAO:
    def __init__(self, session: Callable[[], Session]):
        self.session = session

    def get_or_create_player(self, player_name: str) -> PlayerOrm:
        with self.session() as db_session:
            player = db_session.scalars(
                select(PlayerOrm).where(PlayerOrm.Name == player_name).limit(1)
            ).first()
            logger.debug(player)
            if not player:
                player = PlayerOrm(Name=player_name)
                db_session.add(player)
                db_session.commit()
                db_session.refresh(player)
            return player

    def get_players_name_by_id(self, player1_id: int, player2_id: int) -> list[str]:
        with self.session() as db_session:
            player1_name = db_session.get(PlayerOrm, player1_id)
            player2_name = db_session.get(PlayerOrm, player2_id)
            return (
                [player1_name.Name, player2_name.Name]
                if player1_name and player2_name
                else ["Unknown"]
            )
