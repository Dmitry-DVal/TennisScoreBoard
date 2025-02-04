# Запуск сервера

import logging

import logging_config  # noqa: F401 # Модуль используется для настройки логов

logger = logging.getLogger("app_logger")


def main():
    logger.debug("Вход в main()")
    logger.info("Программа запущена!")


def main_two():
    logger.error("main_two - ошибка!")
    logger.debug("main_two - отладка")


if __name__ == '__main__':
    main()
    main_two()

    logger.info("info message")
    logger.debug("debug message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

# Todo:
#   Как запускается сервер
#   Запуск сервера
#       Понять какой я буду использовать
#           аыв
# dfsdjl
