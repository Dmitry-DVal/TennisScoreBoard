import logging
import urllib.parse
from typing import Callable

from pydantic import ValidationError

from tennis_app.exceptions import DateValidationError
from tennis_app.handlers import RequestHandler
from tennis_app.services import PlayerService

logger = logging.getLogger("app_logger")


class NewMatchHandler(RequestHandler):
    """Handler for the new match creation page."""

    def handle_get(self, environ: dict, start_response: Callable) -> list[bytes]:
        response_body = self.render_template("new_match.html")
        return self.make_response(start_response, response_body)

    @RequestHandler.exception_handler  # type: ignore[arg-type]
    def handle_post(self, environ: dict, start_response: Callable) -> list[bytes]:
        request_body = environ["wsgi.input"].read().decode("utf-8")
        logger.debug(f"Request body {request_body}")
        data = urllib.parse.parse_qs(request_body)

        try:
            match_uuid = PlayerService(data).handle_match_creation()
        except ValidationError:
            return self.handle_exception(start_response, DateValidationError(data))
        except ValueError:
            return self.handle_exception(
                start_response,
                DateValidationError("Players' names must not be the same"),
            )

        logger.debug(f"Match uuid {match_uuid}")
        start_response(
            "303 See Other", [("Location", f"/match-score?uuid={match_uuid}")]
        )
        return []
