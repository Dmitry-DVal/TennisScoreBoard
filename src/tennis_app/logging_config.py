import logging.config
import os

from tennis_app.config import BASE_DIR

log_dir = os.path.join(BASE_DIR, "logs")

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "std_format": {
            "format": "{asctime} - {levelname} - {name}  - {pathname} - {module} - {message}:{lineno}",
            "style": "{",
        },
        "simple_format": {
            "format": "{asctime} - {levelname} - {module}:{lineno} - {message}",
            "style": "{",
            "datefmt": "%H:%M:%S",
        },
        "color_format": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s - %(levelname)s - %(module)s:%(lineno)s - %(message)s",
            "datefmt": "%H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "color_format",
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": os.path.join(log_dir, "debug.log"),
            "formatter": "simple_format",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 1,
            "encoding": "utf8",
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": os.path.join(log_dir, "error.log"),
            "formatter": "std_format",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 1,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "app_logger": {
            "level": "DEBUG",
            "handlers": ["console", "error_file_handler", "debug_file_handler"],
            "propagate": False,
        }
    },
}

logging.config.dictConfig(LOG_CONFIG)
