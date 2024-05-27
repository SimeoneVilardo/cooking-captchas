import base64
import json
import secrets
import string
from database import captcha, schemas, models
from database.core import get_db
from captcha.image import ImageCaptcha
from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from config.settings import settings


router = APIRouter(prefix="/captcha")


def generate_secure_string(length: int = settings.captcha_length) -> string:
    secure_string: string = "".join(secrets.choice(settings.alphabet) for _ in range(length))
    return secure_string


@router.get("/")
def get_captcha(request: Request, db: Session = Depends(get_db)) -> Response:
    secure_string: string = generate_secure_string()
    db_captcha: models.DBCaptcha = captcha.generate_captcha(db, schemas.CreateCaptcha(value=secure_string))
    image = ImageCaptcha()
    image_bytes = image.generate(secure_string)
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
    response = {"image": image_base64, "id": db_captcha.id}
    return Response(
        content=json.dumps(response),
        media_type="application/json",
    )
