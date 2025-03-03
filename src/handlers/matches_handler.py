import urllib.parse

from src.handlers.base_handler import RequestHandler, logger
from src.services.match_service import MatchService


class MatchesHandler(RequestHandler):
    """Обработчик страницы завершенных матчей."""

    def __init__(self):
        self.match_service = MatchService()

    def handle_get(self, environ, start_response):
        data = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
        logger.debug(f"Полученные данные в GET {data}")

        if data:  # Если словарь не пустой
            response_body = self.render_template("completed_matches.html")

        else:

            logger.debug(f"Делаем запрос всех завершенных матчей")
            matches = self.match_service.get_completed_matches()
            print(matches)

            response_body = self.render_template("completed_matches.html",
                                                 matches=matches)

            return self.make_response(start_response, response_body)

        return self.make_response(start_response, response_body)

    def handle_post(self, environ, start_response):
        return self.make_response(start_response, b"Method Not Allowed",
                                  "405 Method Not Allowed")
