import os

# Основные пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Настройки сервера
HOST = "127.0.0.1"
PORT = 8000
