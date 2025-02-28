from src.handlers.base_handler import RequestHandler


class IndexHandler(RequestHandler):
    """Обработчик главной страницы."""

    def handle_get(self, environ, start_response):
        response_body = self.render_template("index.html")
        return self.make_response(start_response, response_body)

    def handle_post(self, environ, start_response):
        return self.make_response(start_response, b"Method Not Allowed",
                                  "405 Method Not Allowed")
