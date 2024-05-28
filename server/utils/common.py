import secrets
import string
from config.settings import settings


def generate_secure_string(length: int = settings.captcha_length) -> string:
    secure_string: string = "".join(secrets.choice(settings.alphabet) for _ in range(length))
    return secure_string
