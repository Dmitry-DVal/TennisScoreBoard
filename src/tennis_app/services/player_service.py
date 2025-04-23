import logging
from typing import Any

from tennis_app.dao import MatchDAO, PlayerDAO
from tennis_app.database import session
from tennis_app.dtos import PlayerDTO


logger = logging.getLogger("app_logger")


class PlayerService:
    def __init__(self, data: dict):
        self.data = data
        self.session_factory = session
        self.player_dao = PlayerDAO(self.session_factory)
        self.match_dao = MatchDAO(self.session_factory)
        logger.debug("Data received: %s", self.data)

    def handle_match_creation(self) -> str:
        player1_dto, player2_dto = self._validate_players()
        player1, player2 = self._get_or_create_players(player1_dto, player2_dto)
        match_uuid = self._create_match(player1, player2)
        return match_uuid

    def _validate_players(self) -> tuple[PlayerDTO, PlayerDTO]:
        first_player = self.data.get("first_player", [""])[0]
        second_player = self.data.get("second_player", [""])[0]

        player1 = PlayerDTO(name=first_player)
        player2 = PlayerDTO(name=second_player)
        logger.debug("Players DTO %s", [player1, player2])

        if player1.name == player2.name:
            raise ValueError
        return player1, player2

    def _get_or_create_players(
        self, player1_dto: PlayerDTO, player2_dto: PlayerDTO
    ) -> tuple[Any, Any]:
        player1 = self.player_dao.get_or_create_player(player1_dto.name)
        player2 = self.player_dao.get_or_create_player(player2_dto.name)

        logger.debug("Players found or created: %s", [player1, player2])
        return player1, player2

    def _create_match(self, player1: Any, player2: Any) -> str:
        match = self.match_dao.create_match(player1.ID, player2.ID)
        logger.debug(f"Match has been successfully created: {match}")
        logger.debug(match.UUID)
        return match.UUID
