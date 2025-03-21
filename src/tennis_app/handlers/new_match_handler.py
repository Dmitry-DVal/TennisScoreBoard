import urllib.parse
from typing import Tuple, Any

from pydantic import ValidationError

from tennis_app.dao import MatchDAO, PlayerDAO
from tennis_app.dtos import PlayerDTO
from tennis_app.exceptions import DateValidationError
from tennis_app.handlers import RequestHandler, logger


class NewMatchHandler(RequestHandler):
    """Handler for the new match creation page."""

    def handle_get(self, environ: dict, start_response) -> list[bytes]:
        response_body = self.render_template("new_match.html")
        return self.make_response(start_response, response_body)

    @RequestHandler.exception_handler
    def handle_post(self, environ: dict, start_response) -> list[bytes]:
        request_body = environ['wsgi.input'].read().decode('utf-8')
        logger.debug(f"Request body {request_body}")
        data = urllib.parse.parse_qs(request_body)

        try:
            player1_dto, player2_dto = self._validate_players(data)
        except ValidationError:
            return self.handle_exception(
                start_response,
                DateValidationError(data))

        if player1_dto.name == player2_dto.name:
            logger.warning(
                f"Player names can't be the same. {player1_dto.name}, {player2_dto.name}")
            return self.handle_exception(
                start_response,
                DateValidationError(f"Players can't be the same. {data}")
            )

        player1, player2 = self._get_or_create_players(player1_dto, player2_dto)

        return self._create_and_redirect(player1, player2, start_response)

    def _validate_players(self, data: dict[str, list[str]]) -> tuple[
        PlayerDTO, PlayerDTO]:
        first_player = data.get("first_player", [""])[0]
        second_player = data.get("second_player", [""])[0]

        player1 = PlayerDTO(name=first_player)
        player2 = PlayerDTO(name=second_player)

        logger.info(f"The validation was successful: {repr(player1)}, {repr(player2)}")
        return player1, player2

    def _get_or_create_players(self, player1_dto: PlayerDTO, player2_dto: PlayerDTO) -> \
            Tuple[Any, Any]:
        player1 = PlayerDAO.get_or_create_player(player1_dto.name)
        player2 = PlayerDAO.get_or_create_player(player2_dto.name)
        logger.debug(f"Players found or created: {player1}, {player2}")
        return player1, player2

    def _create_and_redirect(self, player1, player2, start_response) -> list[bytes]:
        match = MatchDAO.create_match(player1.ID, player2.ID)
        logger.debug(f"Match has been successfully created: {match}")
        return self.redirect(start_response, f"/match-score?uuid={match.UUID}")

    def redirect(self, start_response, location: str) -> list[bytes]:
        logger.info(f"Redirect {location}")
        start_response("303 See Other", [("Location", location)])
        return []
