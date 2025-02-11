"""
Базовый класс
Рендеринг шаблонов
Общие методы (например, обработка ошибок)
В будущем сюда можно добавить поддержку POST-запросов

Остальные обработчики наследуются от него.
"""

from abc import abstractmethod, ABC

from jinja2 import Environment, FileSystemLoader

from src.config import TEMPLATES_DIR


class BaseHandler(ABC):
    # Настройка Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def render_template(self, template_name):
        """Рендерит HTML-шаблон"""
        template = self.env.get_template(template_name)
        return template.render().encode("utf-8")

    @abstractmethod
    def handle_request(self, environ, start_response):
        """Общий метод, который должны переопределять все обработчики"""
        pass
