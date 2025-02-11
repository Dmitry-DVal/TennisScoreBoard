from src.handlers.base_handler import BaseHandler


class NewMatchHandler(BaseHandler):
    """Обработчик страницы создания нового матча."""

    def handle_request(self, environ, start_response):
        response_body = self.render_template("new_match.html")
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body]
