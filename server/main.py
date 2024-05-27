from fastapi import FastAPI
from routers.captcha import router as captcha_router
from database import models
from database.core import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(captcha_router)


@app.get("/")
async def index():
    return {"message": "Hello Cooking Captchas"}
