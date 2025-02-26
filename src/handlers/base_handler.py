import logging
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
