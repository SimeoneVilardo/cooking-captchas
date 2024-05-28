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


class CaptchaResponse(BaseModel):
    detail: str

    class Config:
        from_attributes = True
