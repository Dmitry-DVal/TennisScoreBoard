import logging

# from paste.translogger import TransLogger
from waitress import serve

import config
import logging_config  # noqa
from router import Router

logger = logging.getLogger("app_logger")

if __name__ == "__main__":
    logger.info(f"Server is running at http://{config.HOST}:{config.PORT}")
    # Можно включить TransLogger
    # wsgi_app = TransLogger(Router.application, setup_console_handler=True)
    # serve(wsgi_app, host=config.HOST, port=config.PORT, _quiet=False)

    serve(Router.application, host=config.HOST, port=config.PORT, _quiet=False)
    logger.info("Server stopped")
