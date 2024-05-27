from fastapi import FastAPI
from routers.captcha import router as captcha_router
from database import models
from database.core import engine
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from routers.limiter import limiter

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(captcha_router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
