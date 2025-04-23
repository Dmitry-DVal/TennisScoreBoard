import logging
import urllib.parse
from typing import Callable

from pydantic import ValidationError

from tennis_app.dtos import PointWinnerDTO
from tennis_app.exceptions import DateValidationError
from tennis_app.handlers import RequestHandler
from tennis_app.services import MatchService

logger = logging.getLogger("app_logger")


class MatchScoreHandler(RequestHandler):
    """Handler for the scoring page."""

    def handle_get(self, environ: dict, start_response: Callable) -> list[bytes]:
        match_id = self.get_uuid_from_request(environ)
        logger.debug("Match UUID received: %s", match_id)

        if match_id is None:
            return self.handle_exception(
                start_response, DateValidationError({"uuid": "Missing match ID"})
            )

        try:
            match_data = MatchService().get_match_data(match_id)
        except ValueError as e:
            return self.handle_exception(start_response, DateValidationError(str(e)))

        response_body = self.render_template(
            "match_score.html",
            match=match_data["match"],
            match_score=match_data["score"],
            player1_name=match_data["player1_name"],
            player2_name=match_data["player2_name"],
        )
        return self.make_response(start_response, response_body)

    @RequestHandler.exception_handler  # type: ignore
    def handle_post(self, environ: dict, start_response: Callable) -> list[bytes]:
        request_body = environ["wsgi.input"].read().decode("utf-8")
        logger.debug(f"POST запрос: {request_body}")
        data = urllib.parse.parse_qs(request_body)
        match_id = self.get_uuid_from_request(environ)

        try:
            player_raw = data.get("player", [""])[0]
            dto = PointWinnerDTO(player=int(player_raw))
        except ValidationError:
            return self.handle_exception(
                start_response, DateValidationError("Invalid request format")
            )
        if match_id is None:
            return self.handle_exception(
                start_response, DateValidationError({"uuid": "Missing match ID"})
            )

        MatchService().update_score(match_id, dto)

        start_response("302 Found", [("Location", f"/match-score?uuid={match_id}")])
        return []
