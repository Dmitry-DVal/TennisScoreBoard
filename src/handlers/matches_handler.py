from src.handlers.base_handler import BaseHandler


class MatchesHandler(BaseHandler):
    """Обработчик страницы завершенных матчей."""

    def handle_request(self, environ, start_response):
        response_body = self.render_template("completed_matches.html")
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body]
