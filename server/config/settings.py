from pydantic import Field
import string
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field("Cooking Captchas")
    openapi_url: str = Field("/openapi.json")
    db_username: str = Field(...)
    db_password: str = Field(...)
    db_host: str = Field(...)
    db_name: str = Field(...)
    captcha_length: int = Field(6)
    alphabet: str = Field("".join(string.ascii_uppercase) + "".join(string.digits))
    validity_minutes: int = Field(5)


settings = Settings()
