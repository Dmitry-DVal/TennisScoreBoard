import logging

from handlers import (IndexHandler, NewMatchHandler, MatchScoreHandler, MatchesHandler,
                      StaticHandler, RequestHandler)
from src.exceptions import NotFoundError

logger = logging.getLogger("app_logger")


class Router:
    """Маршрутизатор запросов."""
    routes = {
        "/": IndexHandler(),
        "/new-match": NewMatchHandler(),
        "/match-score": MatchScoreHandler(),
        "/matches": MatchesHandler(),
    }

    @classmethod
    def application(cls, environ, start_response):
        """Вызов нужного обработчика по URL."""
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET")

        if path.startswith("/static/"):
            return StaticHandler().handle_get(environ, start_response)

        handler = cls.routes.get(path)
        if handler:
            logger.info(f"Запрос {method}: {path}")
            return handler.handle_request(environ, start_response)
        else:
            return RequestHandler().handle_exception(start_response,
                                                     NotFoundError(path))
