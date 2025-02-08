import logging

from handlers import handle_index, handle_new_match, handle_matches, handle_match_score
from static_handler import serve_static

logger = logging.getLogger("app_logger")


def application(environ, start_response):
    """Определяет, какой обработчик вызывать"""

    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    # logger.debug(f"environ = {environ}, start_response = {start_response}")
    logger.info(f"Запрос: {method} {path}")

    if path == "/":
        return handle_index(environ, start_response)
    elif path == "/new-match":
        return handle_new_match(environ, start_response)
    elif path == "/matches":
        return handle_matches(environ, start_response)
    elif path == "/match-score":
        return handle_match_score(environ, start_response)
    elif path.startswith("/static/"):
        return serve_static(environ, start_response)
    else:
        response_body = b"404 Not Found"
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [response_body]
