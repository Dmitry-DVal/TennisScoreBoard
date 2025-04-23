import logging
import os
from typing import Callable

from tennis_app.config import STATIC_DIR
from tennis_app.handlers.base_handler import RequestHandler

logger = logging.getLogger("app_logger")


class StaticHandler(RequestHandler):
    """Handler for static file distribution."""

    def handle_get(self, environ: dict, start_response: Callable) -> list[bytes]:
        path = environ.get("PATH_INFO", "/")

        if path == "/favicon.ico":
            path = "/static/favicon.ico"

        file_path = os.path.join(STATIC_DIR, path[len("/static/") :])

        if os.path.exists(file_path) and os.path.isfile(file_path):
            return self.serve_static(start_response, file_path)
        return []

    def serve_static(self, start_response: Callable, file_path: str) -> list[bytes]:
        with open(file_path, "rb") as f:
            response_body = f.read()

        content_type = self.get_content_type(file_path)
        return self.make_response(start_response, response_body, "200 OK", content_type)

    @staticmethod
    def get_content_type(file_path: str) -> str:
        ext_map = {
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".ico": "image/x-icon",
        }
        return ext_map.get(os.path.splitext(file_path)[1], "application/octet-stream")
