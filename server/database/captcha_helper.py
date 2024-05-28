import datetime
from sqlalchemy.orm import Session
from config.settings import settings

from database import models, schemas
from utils.common import ManagedException


class CaptchaBaseException(ManagedException):
    pass


class CaptchaNotFoundException(CaptchaBaseException):
    def __init__(self, detail="Captcha not found", status_code=404):
        super().__init__(detail, status_code)


class CaptchaAlreadySolvedException(CaptchaBaseException):
    def __init__(self, detail="Captcha has already been solved", status_code=409):
        super().__init__(detail, status_code)


class CaptchaExpiredException(CaptchaBaseException):
    def __init__(self, detail="Captcha has expired", status_code=400):
        super().__init__(detail, status_code)


class CaptchaInvalidException(CaptchaBaseException):
    def __init__(self, detail="Captcha is invalid", status_code=400):
        super().__init__(detail, status_code)


def get_captcha(db: Session, id: int):
    captcha = db.query(models.DBCaptcha).filter(models.DBCaptcha.id == id).first()
    if captcha is None:
        raise CaptchaNotFoundException()
    return captcha


def generate_captcha(db: Session, captcha: schemas.CreateCaptcha) -> models.DBCaptcha:
    db_captcha = models.DBCaptcha(value=captcha.value)
    db.add(db_captcha)
    db.commit()
    db.refresh(db_captcha)
    return db_captcha


def validate_captcha(db: Session, user_captcha: schemas.ReadCaptcha, db_captcha: models.DBCaptcha):
    _check_captcha(user_captcha, db_captcha)
    db_captcha.is_used = True
    db.commit()
    db.refresh(db_captcha)
    return db_captcha


def _check_captcha(user_captcha: schemas.ReadCaptcha, db_captcha: models.DBCaptcha) -> None:
    if db_captcha.created_at < datetime.datetime.now() - datetime.timedelta(settings.validity_minutes):
        raise CaptchaExpiredException()
    if db_captcha.is_used:
        raise CaptchaAlreadySolvedException()
    if db_captcha.value != user_captcha.value:
        raise CaptchaInvalidException()
