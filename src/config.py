import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("app_logger")

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_pymysql(self):
        dsn = f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        logger.info(f"DSN configuration {dsn}")
        return dsn

    model_config = SettingsConfigDict(env_file=env_path)


settings_db = Settings()

# Main paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Server settings
HOST = "127.0.0.1"
PORT = 8000
