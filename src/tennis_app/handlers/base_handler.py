import logging
import urllib.parse
from abc import abstractmethod, ABC

from jinja2 import Environment, FileSystemLoader
from sqlalchemy.exc import IntegrityError

from tennis_app.config import TEMPLATES_DIR
from tennis_app.exceptions import AppError, MethodNotAllowed, DatabaseError

logger = logging.getLogger("app_logger")


class BaseHandler(ABC):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def render_template(self, template_name, **kwargs):
        template = self.env.get_template(template_name)
        return template.render(**kwargs).encode("utf-8")

    @abstractmethod
    def handle_request(self, environ, start_response):
        pass

    @abstractmethod
    def handle_get(self, environ, start_response):
        pass

    @abstractmethod
    def handle_post(self, environ, start_response):
        pass

    def make_response(self, start_response, body: bytes, status="200 OK",
                      content_type="text/html"):
        start_response(status, [("Content-Type", f"{content_type}; charset=utf-8")])
        return [body]


class RequestHandler(BaseHandler):

    def handle_request(self, environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET")
        if method == "POST":
            return self.handle_post(environ, start_response)
        elif method == "GET":
            return self.handle_get(environ, start_response)
        else:
            return self.handle_exception(start_response, MethodNotAllowed(method))

    def get_uuid_from_request(self, environ) -> str | None:
        return \
            urllib.parse.parse_qs(environ.get("QUERY_STRING", "")).get("uuid", [None])[
                0]

    def handle_exception(self, start_response, error: AppError):
        """Centralized error handling."""
        logger.error(f"Error {error.status_code}: {error}")

        response_body = self.render_template("error.html", error_message=error.message)
        return self.make_response(start_response, response_body, error.status_code)

    def exception_handler(method):
        """A decorator for handling common errors."""

        def wrapper(self, environ, start_response, *args, **kwargs):
            try:
                return method(self, environ, start_response, *args, **kwargs)
            except IntegrityError:
                return self.handle_exception(start_response, DatabaseError())
            except Exception:
                return self.handle_exception(start_response, AppError())

        return wrapper

    def handle_get(self, environ, start_response):
        pass

    def handle_post(self, environ, start_response):
        pass
