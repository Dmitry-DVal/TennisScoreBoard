import urllib.parse

from sqlalchemy.exc import ProgrammingError

from src.dao import MatchDAO
from src.exceptions import DateValidationError, MethodNotAllowed
from src.handlers import RequestHandler, logger


class MatchesHandler(RequestHandler):
    """Handler for the completed matches page."""
    MAX_MATCHERS_PER_PAGE = 5

    def handle_get(self, environ: dict, start_response) -> list[bytes]:
        data = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
        logger.debug(f"Received data in GET {data}")

        player_name = data.get('filter_by_player_name', [None])[0]
        try:
            page = int(data.get('page', [1])[0])

            matches, total_pages = MatchDAO().get_completed_matches(
                player_name=player_name,
                page=page,
                per_page=self.MAX_MATCHERS_PER_PAGE
            )
            if page > total_pages:
                logger.warning(
                    f"The user requested a non-existent page ({page}).")
                raise ValueError


        except ValueError:
            return self.handle_exception(start_response, DateValidationError(data))
        except ProgrammingError:
            return self.handle_exception(start_response, DateValidationError(data))

        logger.debug(f"Filter by player: {player_name}, Page: {page}")

        response_body = self.render_template(
            "completed_matches.html",
            matches=matches,
            current_page=page,
            total_pages=total_pages,
            filter_by_player_name=player_name
        )

        return self.make_response(start_response, response_body)

    def handle_post(self, environ: dict, start_response):
        return self.handle_exception(start_response, MethodNotAllowed("POST"))

    def redirect(self, start_response, location: str) -> list[bytes]:
        logger.info(f"Redirect {location}")
        start_response("303 See Other", [("Location", location)])
        return []
