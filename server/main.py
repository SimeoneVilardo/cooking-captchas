from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from routers.captcha import router as captcha_router
from database import models
from database.core import engine
from slowapi.errors import RateLimitExceeded
from routers.limiter import limiter
from config.settings import settings

app = FastAPI(openapi_url=settings.openapi_url)

models.Base.metadata.create_all(bind=engine)

app.include_router(captcha_router)

app.state.limiter = limiter


# TODO: This is an ugly (?) workaround to make mypy happy
# I would like to use:
# from slowapi import _rate_limit_exceeded_handler
# But mypy raises an error: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type...
# If any strange behavior occurs, this is the first place to look
async def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})


app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
