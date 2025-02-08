import logging

from paste.translogger import TransLogger
from waitress import serve

import config
import logging_config  # noqa
from router import application

logger = logging.getLogger("app_logger")

if __name__ == "__main__":
    logger.info(f"Server is running at http://{config.HOST}:{config.PORT}")
    wsgi_app = TransLogger(application, setup_console_handler=True)
    serve(wsgi_app, host=config.HOST, port=config.PORT, _quiet=False)
    logger.info("Server stopped")
