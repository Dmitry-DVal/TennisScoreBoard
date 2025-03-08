class AppError(Exception):
    """Базовое исключение приложения"""
    status_code = "500 Internal Server Error"
    message = "Произошла ошибка"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class MethodNotAllowed(AppError):
    def __init__(self, method):
        self.status_code = "405 Method Not Allowed"
        message = f'Method {method} Not Allowed.'
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, path, *args):
        self.status_code = "404 Not Found"
        message = f'Requested path "{path}" was not found.'
        super().__init__(message)

