from datetime import datetime, timedelta
from typing import Dict, Generator
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from database.core import get_db
from database import models
from main import app
from utils.captcha_generator import CaptchaGenerator, FakeSecureStringGenerator, get_captcha_generator

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> Generator[Session, None, None]:
    models.Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

    yield db_session
    db_session.close()
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def simple_captchas(session: Session) -> Generator[Dict[int, models.DBCaptcha], None, None]:
    captchas = [
        models.DBCaptcha(id=1, value="COOKING", is_used=False, created_at=datetime.now()),
        models.DBCaptcha(id=2, value="COOKING", is_used=True, created_at=datetime.now()),
        models.DBCaptcha(id=3, value="COOKING", is_used=False, created_at=datetime.now() - timedelta(days=1)),
    ]
    session.add_all(captchas)
    session.commit()
    yield {captcha.id: captcha for captcha in captchas}
    session.expunge_all()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_captcha_generator():
    return CaptchaGenerator(FakeSecureStringGenerator("COOKING"))


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_captcha_generator] = override_get_captcha_generator

client = TestClient(app)


@pytest.mark.parametrize(
    "id,value,expected",
    [
        (1, "COOKING", 200),
        (1, "ROBOT", 403),
        (3, "COOKING", 403),
        (2, "COOKING", 409),
        (4, "COOKING", 404),
    ],
)
def test_validate_captcha(session, simple_captchas, id, value, expected):
    response = client.post("/captcha/", json={"id": id, "value": value})
    assert response.status_code == expected
    result = response.json()
    assert isinstance(result["detail"], str)
