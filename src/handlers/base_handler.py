import logging
import urllib.parse
from abc import abstractmethod, ABC

from jinja2 import Environment, FileSystemLoader

from src.config import TEMPLATES_DIR

logger = logging.getLogger("app_logger")


class BaseHandler(ABC):
    # Настройка Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def render_template(self, template_name, **kwargs):
        """Рендерит HTML-шаблон"""
        template = self.env.get_template(template_name)
        return template.render(**kwargs).encode("utf-8")

    @abstractmethod
    def handle_request(self, environ, start_response):
        """Общий метод, который должны переопределять все обработчики"""
        pass

    def make_response(self, start_response, body: bytes, status="200 OK",
                      content_type="text/html"):
        """Формирует HTTP-ответ"""
        start_response(status, [("Content-Type", f"{content_type}; charset=utf-8")])
        return [body]


class RequestHandler(BaseHandler):
    """Обработчик, который автоматически определяет тип запроса (GET/POST)"""

    def handle_request(self, environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET")
        if method == "POST":
            return self.handle_post(environ, start_response)
        return self.handle_get(environ, start_response)

    def get_uuid_from_request(self, environ) -> str | None:
        """Получает UUID из GET-параметров"""
        return \
            urllib.parse.parse_qs(environ.get("QUERY_STRING", "")).get("uuid", [None])[
                0]

    @abstractmethod
    def handle_get(self, environ, start_response):
        pass

    @abstractmethod
    def handle_post(self, environ, start_response):
        pass

    def error_response(self, start_response, message: str, status: str):
        """Генерация ошибки"""
        logger.error(f"Ошибка - {message}, {status}")
        start_response(status, [("Content-Type", "text/plain")])
        return [message.encode("utf-8")]
