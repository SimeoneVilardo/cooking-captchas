from fastapi import FastAPI
from database import models
from database.core import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def index():
    return {"message": "Hello Cooking Captchas"}
