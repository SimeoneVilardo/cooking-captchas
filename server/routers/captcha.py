import datetime
import json
from database import schemas, models
from database.core import get_db
from captcha.image import ImageCaptcha
from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from database import captcha_helper
from routers.limiter import limiter
from config.settings import settings
from utils.captcha_generator import CaptchaGenerator, get_captcha_generator
from utils.common import exception_handler
from utils.captcha_response import get_response_handler


router = APIRouter(prefix="/captcha")
image_generator = ImageCaptcha()


@router.get(
    "/",
    responses={
        200: {
            "description": "Captcha image",
            "content": {
                "application/json": {"example": {"image": "base64encodedimage", "id": 1}},
                "image/png": {"schema": {"type": "string", "format": "binary"}, "example": "(binary image data)"},
            },
            "headers": {"X-Captcha-ID": {"description": "ID of the captcha", "schema": {"type": "integer"}}},
        },
        406: {"description": "Unsupported accept header", "model": schemas.CaptchaResponse},
    },
    summary="Get Captcha",
    description="Get a new captcha image.",
)
@limiter.limit("10/minute", key_func=lambda: "get_captcha")
@exception_handler()
def get_captcha(
    request: Request,
    db: Session = Depends(get_db),
    captcha_generator: CaptchaGenerator = Depends(get_captcha_generator),
) -> Response:
    accept_header = request.headers.get("accept", "*/*")
    response_handler = get_response_handler(accept_header)
    captcha = captcha_generator.get_captcha()
    image, secure_string = captcha["image"], captcha["value"]
    db_captcha: models.DBCaptcha = captcha_helper.create_captcha(db, schemas.CreateCaptcha(value=secure_string))
    return response_handler.handle(image, db_captcha.id)


@router.post(
    "/",
    response_model=schemas.CaptchaResponse,
    responses={
        200: {"description": "Captcha validated successfully", "model": schemas.CaptchaResponse},
        403: {"description": "Captcha invalid", "model": schemas.CaptchaResponse},
        403: {"description": "Captcha has expired", "model": schemas.CaptchaResponse},
        404: {"description": "Captcha not found", "model": schemas.CaptchaResponse},
        409: {"description": "Captcha already used", "model": schemas.CaptchaResponse},
    },
    summary="Validate Captcha",
    description="Validate the captcha value provided by the user.",
)
@limiter.limit("10/minute", key_func=lambda: "post_captcha")
@exception_handler()
def post_captcha(request: Request, captcha: schemas.ReadCaptcha, db: Session = Depends(get_db)) -> Response:
    db_captcha = captcha_helper.find_captcha(db, captcha.id)
    if (datetime.datetime.now() - db_captcha.created_at) > datetime.timedelta(seconds=settings.validity_seconds):
        raise captcha_helper.CaptchaExpiredException()
    if db_captcha.is_used:
        raise captcha_helper.CaptchaAlreadySolvedException()
    if db_captcha.value != captcha.value:
        raise captcha_helper.CaptchaInvalidException()
    captcha_helper.update_captcha(db, db_captcha.id, schemas.UpdateCaptcha(is_used=True))
    return Response(
        content=json.dumps({"detail": "Captcha validated successfully"}),
        media_type="application/json",
    )
