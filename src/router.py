import logging

from handlers import (IndexHandler, NewMatchHandler, MatchScoreHandler, MatchesHandler,
                      serve_static)


logger = logging.getLogger("app_logger")


class Router:
    """Маршрутизатор запросов."""
    routes = {
        "/": IndexHandler(),
        "/new-match": NewMatchHandler(),
        "/match-score": MatchScoreHandler(),
        "/matches": MatchesHandler()
    }

    @classmethod
    def application(cls, environ, start_response):
        """Вызов нужного обработчика по URL."""
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET")

        logger.debug(f"Запрос: {method} {path}")

        if path.startswith("/static/"):
            return serve_static(environ, start_response)

        handler = cls.routes.get(path)
        if handler:
            logger.info(f"Запрос {method}: {path}")
            return handler.handle_request(environ, start_response)
        else:
            response_body = b"404 Not Found"
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [response_body]
