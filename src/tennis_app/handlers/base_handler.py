import logging
import urllib.parse
from abc import abstractmethod, ABC

from jinja2 import Environment, FileSystemLoader
from sqlalchemy.exc import IntegrityError

from tennis_app.config import TEMPLATES_DIR
from tennis_app.exceptions import AppError, MethodNotAllowed, DatabaseError
from typing import Any, Callable

logger = logging.getLogger("app_logger")


class BaseHandler(ABC):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    # def render_template(self, template_name, **kwargs):
    def render_template(self, template_name: str, **kwargs: Any) -> bytes:
        template = self.env.get_template(template_name)
        return template.render(**kwargs).encode("utf-8")

    @abstractmethod
    def handle_request(self, environ: dict, start_response: Callable) -> list[bytes]:
        pass

    @abstractmethod
    def handle_get(self, environ: dict, start_response: Callable) -> list[bytes]:
        pass

    @abstractmethod
    def handle_post(self, environ: dict, start_response: Callable) -> list[bytes]:
        pass

    def make_response(
        self,
        start_response: Callable,
        body: bytes,
        status: str = "200 OK",
        content_type: str = "text/html",
    ) -> list[bytes]:
        start_response(status, [("Content-Type", f"{content_type}; charset=utf-8")])
        return [body]


class RequestHandler(BaseHandler):
    def handle_request(self, environ: dict, start_response: Callable) -> list[bytes]:
        method = environ.get("REQUEST_METHOD", "GET")
        if method == "POST":
            return self.handle_post(environ, start_response)
        elif method == "GET":
            return self.handle_get(environ, start_response)
        else:
            return self.handle_exception(start_response, MethodNotAllowed(method))

    def get_uuid_from_request(self, environ: dict) -> str | None:
        return urllib.parse.parse_qs(environ.get("QUERY_STRING", "")).get(
            "uuid", [None]
        )[0]

    def handle_exception(
        self, start_response: Callable, error: AppError
    ) -> list[bytes]:
        """Centralized error handling."""
        logger.error(f"Error {error.status_code}: {error}")

        response_body = self.render_template("error.html", error_message=error.message)
        return self.make_response(start_response, response_body, error.status_code)

    def exception_handler(method):  # type: ignore
        """A decorator for handling common errors."""

        def wrapper(  # type: ignore
            self,
            environ: dict[str, Any],
            start_response: Callable,
            *args: Any,
            **kwargs: Any,
        ) -> list[bytes]:  # type: ignore
            try:
                return method(self, environ, start_response, *args, **kwargs)  # type: ignore
            except IntegrityError:
                return self.handle_exception(start_response, DatabaseError())
            except Exception:
                return self.handle_exception(start_response, AppError())

        return wrapper

    def handle_get(self, environ: dict, start_response: Callable) -> list[bytes]:
        raise NotImplementedError

    def handle_post(self, environ: dict, start_response: Callable) -> list[bytes]:
        raise NotImplementedError
