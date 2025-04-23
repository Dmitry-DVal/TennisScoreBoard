import logging
from typing import Any

from tennis_app.dao import MatchDAO, PlayerDAO
from tennis_app.database import session
from tennis_app.dtos import PointWinnerDTO

logger = logging.getLogger("app_logger")


class MatchService:
    def __init__(self) -> None:
        self.session_factory = session
        self.player_dao = PlayerDAO(self.session_factory)
        self.match_dao = MatchDAO(self.session_factory)

    def get_match_data(self, match_id: str) -> dict:
        logger.debug("Obtaining match data: %s", match_id)
        match = self.match_dao.get_match_by_uuid(match_id)

        if not match:
            logger.debug("Match with UUID not found %s", match_id)
            raise ValueError(f"Match {match_id} not found")

        score = match.Score
        player1_name, player2_name = self.player_dao.get_players_name_by_id(
            match.Player1, match.Player2
        )

        logger.debug(
            f"Match: {match}, Score: {score}, Players: {player1_name}, {player2_name}"
        )

        return {
            "match": match,
            "score": score,
            "player1_name": player1_name,
            "player2_name": player2_name,
        }

    def update_score(self, match_id: str, dto: PointWinnerDTO) -> None:
        logger.debug(f"Update match score {match_id}, point winner: {dto.player}")
        self.match_dao.update_match_score(match_id, dto.player)

    def get_completed_matches(
        self,
        player_name: str | None = None,
        page: int = 1,
        per_page: int = 5,
    ) -> tuple[list[Any], int]:
        result = self.match_dao.get_completed_matches(player_name, page, per_page)
        return result
