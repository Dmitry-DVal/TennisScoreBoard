import logging
import os
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("app_logger")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

env_path = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_pymysql(self) -> str:
        dsn = f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        logger.info(f"DSN configuration {dsn}")
        return dsn

    model_config = SettingsConfigDict(env_file=env_path)


settings_db = Settings()  # type: ignore

# Main paths
TEMPLATES_DIR = os.path.join(BASE_DIR, "src", "tennis_app", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "src", "tennis_app", "static")

# Server settings
HOST = "127.0.0.1"
PORT = 8000
