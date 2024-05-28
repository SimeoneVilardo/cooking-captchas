import json
from fastapi.responses import JSONResponse, StreamingResponse
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
from utils.common import generate_secure_string
from utils.captcha_response import UnsupportedAcceptHeaderException, get_response_handler


router = APIRouter(prefix="/captcha")
image_generator = ImageCaptcha()


@router.get(
    "/",
    responses={
        200: {
            "description": "Captcha image",
            "content": {
                "application/json": {"example": {"image": "base64encodedimage", "id": 1}},
                "image/jpeg": {"schema": {"type": "string", "format": "binary"}, "example": "(binary image data)"},
            },
            "headers": {"X-Captcha-ID": {"description": "ID of the captcha", "schema": {"type": "integer"}}},
        },
        406: {"description": "Unsupported accept header", "model": schemas.CaptchaResponse},
    },
    summary="Get Captcha",
    description="Get a new captcha image.",
)
@limiter.limit("10/minute", key_func=lambda: "get_captcha")
def get_captcha(request: Request, db: Session = Depends(get_db)) -> Response:
    accept_header = request.headers.get("accept")
    try:
        response_handler = get_response_handler(accept_header)
    except UnsupportedAcceptHeaderException as e:
        raise HTTPException(status_code=406, detail="Unsupported accept header")
    secure_string: str = generate_secure_string()
    db_captcha: models.DBCaptcha = captcha_helper.generate_captcha(db, schemas.CreateCaptcha(value=secure_string))
    image_bytes = image_generator.generate(secure_string)
    return response_handler.handle(image_bytes, db_captcha.id)


@router.post(
    "/",
    response_model=schemas.CaptchaResponse,
    responses={
        200: {"description": "Captcha validated successfully", "model": schemas.CaptchaResponse},
        400: {"description": "Bad Request", "model": schemas.CaptchaResponse},
        404: {"description": "Captcha not found", "model": schemas.CaptchaResponse},
        409: {"description": "Captcha already used", "model": schemas.CaptchaResponse},
    },
    summary="Validate Captcha",
    description="Validate the captcha value provided by the user.",
)
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
