import os
import string
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Cooking Captchas"
    db_username: str = os.getenv("DB_USERNAME", None)
    db_password: str = os.getenv("DB_PASSWORD", None)
    db_host: str = os.getenv("DB_HOST", None)
    db_name: str = os.getenv("DB_NAME", None)
    captcha_length: int = 6
    alphabet: str = "".join(string.ascii_uppercase) + "".join(string.digits)


settings = Settings()
