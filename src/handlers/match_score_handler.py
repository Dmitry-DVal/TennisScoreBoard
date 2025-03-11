import urllib.parse

from pydantic import ValidationError

from src.dao import MatchDAO, PlayerDAO
from src.dtos import PointWinnerDTO
from src.exceptions import DateValidationError
from src.handlers.base_handler import RequestHandler, logger


class MatchScoreHandler(RequestHandler):
    """Handler for the scoring page."""

    def handle_get(self, environ: dict, start_response) -> list[bytes]:
        match_id = self.get_uuid_from_request(environ)
        match = MatchDAO.get_match_by_uuid(match_id)

        logger.debug(
            f"Requesting player names, accounts from the service to render pages")

        if not match:
            return self.handle_exception(
                start_response,
                DateValidationError(f"There's no such match: {match_id}")
            )

        match_score = match.Score

        player1_name, player2_name = PlayerDAO().get_players_name_by_id(
            match.Player1,
            match.Player2
        )

        response_body = self.render_template(
            "match_score.html",
            match=match,
            match_score=match_score,
            player1_name=player1_name,
            player2_name=player2_name
        )

        return self.make_response(start_response, response_body)

    @RequestHandler.exception_handler
    def handle_post(self, environ: dict, start_response) -> list[bytes]:
        request_body = environ['wsgi.input'].read().decode('utf-8')
        logger.debug(f"Request body {request_body}")
        data = urllib.parse.parse_qs(request_body)

        match_id = self.get_uuid_from_request(environ)

        try:
            validated_data = PointWinnerDTO(player=data.get("player", [""])[0])
        except ValidationError:
            return self.handle_exception(
                start_response,
                DateValidationError(f"Incorrect request form  or player index {data}"))

        MatchDAO().update_match_score(match_id, validated_data.player)

        logger.debug(f"Validated data: {validated_data} - Won a point")

        response_headers = [
            ('Location', f'/match-score?uuid={match_id}'),
            ('Content-Type', 'text/html'),
        ]
        start_response('302 Found', response_headers)

        return []

