from typing import Callable

from tennis_app.exceptions import MethodNotAllowed
from tennis_app.handlers import RequestHandler


class IndexHandler(RequestHandler):
    """Home page handler."""

    def handle_get(self, environ: dict, start_response: Callable) -> list[bytes]:
        response_body = self.render_template("index.html")
        return self.make_response(start_response, response_body)

    def handle_post(self, environ: dict, start_response: Callable) -> list[bytes]:
        return self.handle_exception(start_response, MethodNotAllowed("POST"))
