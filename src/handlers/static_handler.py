import logging
import os

from src.config import STATIC_DIR

logger = logging.getLogger("app_logger")


def serve_static(environ, start_response):
    """Обработчик для раздачи статических файлов"""

    path = environ.get("PATH_INFO", "/")
    file_path = os.path.join(STATIC_DIR, path[len("/static/"):])

    logger.debug(f"Запрос статики: {path} → {file_path}")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            response_body = f.read()

        # Определяем Content-Type
        content_type = "application/octet-stream"
        if file_path.endswith(".css"):
            content_type = "text/css"
        elif file_path.endswith(".js"):
            content_type = "application/javascript"
        elif file_path.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            content_type = "image/png"

        start_response("200 OK", [("Content-Type", content_type)])
        return [response_body]
    else:
        logger.error(f"Файл не найден: {file_path}")
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"404 Not Found"]
