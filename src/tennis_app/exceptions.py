class AppError(Exception):
    """Basic application exception."""

    status_code = "500 Internal Server Error"
    message = "There was an error."

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)


class MethodNotAllowed(AppError):
    """Method Not Allowed error(404)."""

    def __init__(self, method: str):
        self.status_code = "405 Method Not Allowed"
        message = f"Method {method} Not Allowed."
        super().__init__(message)


class NotFoundError(AppError):
    """Page Not Found error(404)."""

    def __init__(self, path: str, *args: object):
        self.status_code = "404 Not Found"
        message = f'Requested path "{path}" was not found.'
        super().__init__(message)


class DateValidationError(AppError):
    """Validation error(400)."""

    def __init__(self, data: dict | str, *args: object):
        self.status_code = "400 Bad Request"
        message = f"Data validation error. {data}."
        super().__init__(message)


class DatabaseError(AppError):
    """Database error(500)."""

    def __init__(self, *args: object):
        self.status_code = "500 Internal Server Error"
        message = "Database error."
        super().__init__(message)
