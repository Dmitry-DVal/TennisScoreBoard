import logging
import os

from src.config import STATIC_DIR
from src.handlers.base_handler import RequestHandler

logger = logging.getLogger("app_logger")


class StaticHandler(RequestHandler):
    """Handler for static file distribution."""

    def handle_get(self, environ: dict, start_response) -> list[bytes]:
        path = environ.get("PATH_INFO", "/")
        file_path = os.path.join(STATIC_DIR, path[len("/static/"):])

        if os.path.exists(file_path) and os.path.isfile(file_path):
            return self.serve_static(start_response, file_path)

    def serve_static(self, start_response, file_path):
        with open(file_path, "rb") as f:
            response_body = f.read()

        content_type = self.get_content_type(file_path)
        return self.make_response(start_response, response_body, "200 OK", content_type)

    @staticmethod
    def get_content_type(file_path) -> str:
        ext_map = {
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        return ext_map.get(os.path.splitext(file_path)[1], "application/octet-stream")
