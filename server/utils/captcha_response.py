from abc import ABC
import abc
import base64
from io import BytesIO
from typing import Dict, Type

from fastapi import Response
from fastapi.responses import JSONResponse, StreamingResponse

from utils.common import ManagedException


class CaptchaResponseHandler(ABC):
    @abc.abstractmethod
    def handle(self, image_bytes: BytesIO, id: int) -> Response: ...


class CaptchaUnsupportedResponseHandler(CaptchaResponseHandler):
    def handle(self, image_bytes: BytesIO, id: int) -> Response:
        raise UnsupportedAcceptHeaderException("Unsupported accept header")


class CaptchaJsonResponseHandler(CaptchaResponseHandler):
    def handle(self, image_bytes: BytesIO, id: int) -> Response:
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
        response_data = {"image": image_base64, "id": id}
        return JSONResponse(content=response_data, headers={"X-Captcha-ID": str(id)})


class CaptchaJpegResponseHandler(CaptchaResponseHandler):
    def handle(self, image_bytes: BytesIO, id: int) -> Response:
        return StreamingResponse(
            content=BytesIO(image_bytes.getvalue()),
            media_type="image/jpeg",
            headers={"X-Captcha-ID": str(id)},
        )


class UnsupportedAcceptHeaderException(ManagedException):
    def __init__(self, detail: str = "Unsupported accept header", status_code: int = 406) -> None:
        super().__init__(detail, status_code)


response_handlers: Dict[str, Type[CaptchaResponseHandler]] = {
    "application/json": CaptchaJsonResponseHandler,
    "*/*": CaptchaJsonResponseHandler,
    "image/jpeg": CaptchaJpegResponseHandler,
}


def get_response_handler(accept_header: str) -> CaptchaResponseHandler:
    handler_class = response_handlers.get(accept_header, CaptchaUnsupportedResponseHandler)
    return handler_class()
