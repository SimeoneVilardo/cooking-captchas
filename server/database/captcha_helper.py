from sqlalchemy.orm import Session

from server.database import models, schemas
from server.utils.common import ManagedException


class CaptchaBaseException(ManagedException):
    pass


class CaptchaNotFoundException(CaptchaBaseException):
    def __init__(self, detail: str = "Captcha not found", status_code: int = 404) -> None:
        super().__init__(detail, status_code)


class CaptchaAlreadySolvedException(CaptchaBaseException):
    def __init__(self, detail: str = "Captcha has already been solved", status_code: int = 409) -> None:
        super().__init__(detail, status_code)


class CaptchaExpiredException(CaptchaBaseException):
    def __init__(self, detail: str = "Captcha has expired", status_code: int = 403) -> None:
        super().__init__(detail, status_code)


class CaptchaInvalidException(CaptchaBaseException):
    def __init__(self, detail: str = "Captcha is invalid", status_code: int = 403) -> None:
        super().__init__(detail, status_code)


def find_captcha(db: Session, id: int) -> models.DBCaptcha:
    captcha = db.query(models.DBCaptcha).filter(models.DBCaptcha.id == id).first()
    if captcha is None:
        raise CaptchaNotFoundException()
    return captcha


def create_captcha(db: Session, captcha: schemas.CreateCaptcha) -> models.DBCaptcha:
    db_captcha = models.DBCaptcha(value=captcha.value)
    db.add(db_captcha)
    db.commit()
    db.refresh(db_captcha)
    return db_captcha


def update_captcha(db: Session, id: int, captcha: schemas.UpdateCaptcha) -> models.DBCaptcha:
    db_captcha = find_captcha(db, id)
    for key, value in captcha.model_dump().items():
        setattr(db_captcha, key, value)
    db.commit()
    db.refresh(db_captcha)
    return db_captcha
