import logging

from tennis_app.exceptions import NotFoundError
from tennis_app.handlers import (IndexHandler, NewMatchHandler, MatchScoreHandler,
                                 MatchesHandler,
                                 StaticHandler, RequestHandler)

logger = logging.getLogger("app_logger")


class Router:
    """Request Router"""
    routes = {
        "/": IndexHandler(),
        "/new-match": NewMatchHandler(),
        "/match-score": MatchScoreHandler(),
        "/matches": MatchesHandler(),
    }

    @classmethod
    def application(cls, environ, start_response):
        """Call the desired handler by URL."""
        path = environ.get("PATH_INFO", "/")
        logger.debug(f"Requested path {path}")
        method = environ.get("REQUEST_METHOD", "GET")

        if path.startswith("/static/") or path.startswith("/favicon.ico"):
            return StaticHandler().handle_get(environ, start_response)

        handler = cls.routes.get(path)
        if handler:
            logger.info(f"Request {method}: {path}")
            return handler.handle_request(environ, start_response)
        else:
            return RequestHandler().handle_exception(start_response,
                                                     NotFoundError(path))
