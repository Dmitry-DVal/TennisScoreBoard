import logging
import os

from src.config import STATIC_DIR
from src.handlers.base_handler import RequestHandler

logger = logging.getLogger("app_logger")


class StaticHandler(RequestHandler):
    """Обработчик для раздачи статических файлов."""

    def handle_get(self, environ, start_response):
        """Определяет, нужно ли раздавать файл или показать 404."""
        path = environ.get("PATH_INFO", "/")
        file_path = os.path.join(STATIC_DIR, path[len("/static/"):])

        if os.path.exists(file_path) and os.path.isfile(file_path):
            return self.serve_static(start_response, file_path)

        return self.error_response(start_response, "Файл не найден", "404 Not Found")

    def serve_static(self, start_response, file_path):
        """Отправляет запрошенный статический файл."""
        with open(file_path, "rb") as f:
            response_body = f.read()

        content_type = self.get_content_type(file_path)
        return self.make_response(start_response, response_body, "200 OK", content_type)

    def handle_post(self, environ, start_response):
        """Отклоняем POST-запросы к статическим файлам."""
        return self.error_response(start_response, "Method Not Allowed",
                                   "405 Method Not Allowed")

    @staticmethod
    def get_content_type(file_path):
        """Определяет тип контента по расширению файла."""
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
