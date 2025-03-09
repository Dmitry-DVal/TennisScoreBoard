import json
import urllib.parse

from pydantic import ValidationError

from src.dao import MatchDAO, PlayerDAO
from src.dtos import PointWinnerDTO
from src.exceptions import DateValidationError
from src.handlers.base_handler import RequestHandler, logger


class MatchScoreHandler(RequestHandler):
    """Handler for the scoring page."""

    def handle_get(self, environ, start_response):
        match_id = self.get_uuid_from_request(environ)
        match = MatchDAO().get_match_by_uuid(match_id)

        logger.debug(
            f"Requesting player names, accounts from the service to render pages")

        if not match:
            return self.handle_exception(start_response, DateValidationError(match_id))

        match_score = self._get_match_score(match)
        player1_name, player2_name = self._get_player_names(match)

        response_body = self.render_template(
            "match_score.html",
            match=match,
            match_score=match_score,
            player1_name=player1_name,
            player2_name=player2_name
        )

        return self.make_response(start_response, response_body)

    @RequestHandler.exception_handler
    def handle_post(self, environ, start_response):
        try:
            request_body = environ['wsgi.input'].read().decode('utf-8')
            logger.debug(f"Request body {request_body}")
            data = urllib.parse.parse_qs(request_body)

            validated_data = PointWinnerDTO(player=data.get("player", [""])[0])
            logger.debug(f"Validated data: {validated_data} - Won a point")

            # Обновляем счёт матча
            match_id = self.get_uuid_from_request(environ)
            updated_match = MatchDAO().update_match_score(
                match_id,
                validated_data.player
            )

            if not updated_match:
                return self.handle_exception(start_response,
                                             DateValidationError(match_id))

            return self.handle_get(environ, start_response)

        except ValidationError:
            return self.handle_exception(start_response, DateValidationError(data))

    def _get_match_score(self, match):
        return json.loads(match.Score) if isinstance(match.Score, str) else match.Score

    def _get_player_names(self, match):
        return PlayerDAO().get_players_name_by_id(
            match.Player1,
            match.Player2
        )
