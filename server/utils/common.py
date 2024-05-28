import secrets
import string
import functools

from fastapi import HTTPException
from config.settings import settings


class ManagedException(Exception):
    def __init__(self, detail, status_code):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def generate_secure_string(length: int = settings.captcha_length) -> string:
    secure_string: string = "".join(secrets.choice(settings.alphabet) for _ in range(length))
    return secure_string


def exception_handler(exception_type=ManagedException, handler=None):
    """
    A decorator that wraps a function to handle exceptions.

    :param exception_type: The type of exception to catch (default is ManagedException).
    :param handler: A function that takes the exception as an argument. If None, it will simply print the exception.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as e:
                if handler:
                    return handler(e)
                else:
                    raise HTTPException(status_code=e.status_code, detail=e.detail)

        return wrapper

    return decorator
