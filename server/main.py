import time
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from server.routers.captcha import router as captcha_router
from server.database import models
from server.database.core import engine
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from server.routers.limiter import limiter
from server.config.settings import settings
from sqlalchemy.exc import OperationalError


app = FastAPI(openapi_url=settings.openapi_url)

#TODO: Investigate better way to wait for db (maybe https://github.com/vishnubob/wait-for-it)
max_retries = 10
attempt = 0

while attempt < max_retries:
    try:
        models.Base.metadata.create_all(bind=engine)
        break  # Exit the loop if successful
    except OperationalError:
        attempt += 1
        if attempt < max_retries:
            time.sleep(1)
    except Exception:
        attempt += 1
        if attempt < max_retries:
            time.sleep(1)

app.include_router(captcha_router)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore[arg-type]
