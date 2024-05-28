from typing import Generator
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from database.core import get_db
from database import models
from main import app
from utils.captcha_generator import CaptchaGenerator, FakeSecureStringGenerator, get_captcha_generator

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        models.Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        models.Base.metadata.drop_all(bind=engine)


def override_get_captcha_generator():
    return CaptchaGenerator(FakeSecureStringGenerator("COOKING"))


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_captcha_generator] = override_get_captcha_generator

client = TestClient(app)


@pytest.mark.parametrize(
    "accept_header",
    [
        ("application/json"),
        ("*/*"),
        (None),
    ],
)
def test_generate_captcha_json(accept_header):
    headers = {"accept": accept_header} if accept_header else {}
    response = client.get("/captcha", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert isinstance(data["image"], str)
    assert isinstance(data["id"], int)
    assert isinstance(response.headers["X-Captcha-ID"], str)
    assert str(data["id"]) == response.headers["X-Captcha-ID"]


@pytest.mark.parametrize(
    "accept_header",
    [
        ("image/png"),
    ],
)
def test_generate_captcha_png(accept_header):
    headers = {"accept": accept_header} if accept_header else {}
    response = client.get("/captcha", headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert isinstance(response.headers["X-Captcha-ID"], str)
    assert response.content[:8] == b"\x89PNG\r\n\x1a\n"
