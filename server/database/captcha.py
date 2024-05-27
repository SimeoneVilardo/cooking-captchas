import datetime
from sqlalchemy.orm import Session
from config.settings import settings

from database import models, schemas


class CaptchaBaseException(Exception):
    pass


class CaptchaNotFoundException(CaptchaBaseException):
    pass


class CaptchaAlreadySolvedException(CaptchaBaseException):
    pass


class CaptchaExpiredException(CaptchaBaseException):
    pass


class CaptchaInvalidException(CaptchaBaseException):
    pass


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
