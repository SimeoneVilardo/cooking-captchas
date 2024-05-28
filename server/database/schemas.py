import datetime
from pydantic import BaseModel


class CaptchaBase(BaseModel):
    pass


class CreateCaptcha(CaptchaBase):
    value: str


class ReadCaptcha(CaptchaBase):
    id: int
    value: str


class UpdateCaptcha(CaptchaBase):
    is_used: bool


class Captcha(CaptchaBase):
    id: int
    value: str
    is_used: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class CaptchaResponse(BaseModel):
    detail: str

    class Config:
        from_attributes = True
