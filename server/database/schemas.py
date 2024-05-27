import datetime
from pydantic import BaseModel


class CaptchaBase(BaseModel):
    value: str


class CreateCaptcha(CaptchaBase):
    pass


class ReadCaptcha(CaptchaBase):
    id: int
    value: str


class Captcha(CaptchaBase):
    id: int
    is_used: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
    status_code: int

    class Config:
        from_attributes = True