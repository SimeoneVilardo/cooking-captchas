import base64
import json
import secrets
import string
from database import schemas, models
from database.captcha_helper import (
    CaptchaNotFoundException,
    CaptchaAlreadySolvedException,
    CaptchaExpiredException,
    CaptchaInvalidException,
)
from database.core import get_db
from captcha.image import ImageCaptcha
from fastapi import APIRouter, HTTPException, Request, Depends, Response
from sqlalchemy.orm import Session
from config.settings import settings
from database import captcha_helper
from routers.limiter import limiter


router = APIRouter(prefix="/captcha")


def generate_secure_string(length: int = settings.captcha_length) -> string:
    secure_string: string = "".join(secrets.choice(settings.alphabet) for _ in range(length))
    return secure_string


@router.get("/")
@limiter.limit("10/minute", key_func=lambda: "get_captcha")
def get_captcha(request: Request, db: Session = Depends(get_db)) -> Response:
    secure_string: string = generate_secure_string()
    db_captcha: models.DBCaptcha = captcha_helper.generate_captcha(db, schemas.CreateCaptcha(value=secure_string))
    image = ImageCaptcha()
    image_bytes = image.generate(secure_string)
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
    response = {"image": image_base64, "id": db_captcha.id}
    return Response(
        content=json.dumps(response),
        media_type="application/json",
    )


@router.post("/")
@limiter.limit("10/minute", key_func=lambda: "post_captcha")
def post_captcha(request: Request, captcha: schemas.ReadCaptcha, db: Session = Depends(get_db)) -> Response:
    try:
        db_captcha = captcha_helper.get_captcha(db, captcha.id)
    except CaptchaNotFoundException as e:
        raise HTTPException(status_code=404, detail="Captcha not found")

    try:
        updated_db_captcha = captcha_helper.validate_captcha(db, captcha, db_captcha)
    except CaptchaExpiredException as e:
        raise HTTPException(status_code=400, detail="Captcha expired")
    except CaptchaAlreadySolvedException as e:
        raise HTTPException(status_code=409, detail="Captcha already used")
    except CaptchaInvalidException as e:
        raise HTTPException(status_code=400, detail="Captcha value incorrect")

    return Response(
        content=json.dumps({"detail": "Captcha validated successfully"}),
        media_type="application/json",
    )
