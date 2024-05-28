from pydantic import Field
import string
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field("Cooking Captchas")
    openapi_url: str = Field("/openapi.json")
    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_name: str = Field(..., env="DB_NAME")
    captcha_length: int = Field(6)
    alphabet: str = Field("".join(string.ascii_uppercase) + "".join(string.digits))
    validity_minutes: int = Field(5)


settings = Settings()
