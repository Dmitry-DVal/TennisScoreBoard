import os

from jinja2 import Environment, FileSystemLoader

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Настройка Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def render_template(template_name):
    """Рендерит HTML-шаблон"""
    template = env.get_template(template_name)
    return template.render().encode("utf-8")


def handle_index(environ, start_response):
    """Главная страница"""
    response_body = render_template("index.html")
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body]


def handle_new_match(environ, start_response):
    """Страница создания нового матча"""
    response_body = render_template("new_match.html")
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body]


def handle_match_score(environ, start_response):
    """Страница подсчета очков"""
    response_body = render_template("match_score.html")
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body]


def handle_matches(environ, start_response):
    """Страница сыгранных матчей"""
    response_body = render_template("completed_matches.html")
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body]
