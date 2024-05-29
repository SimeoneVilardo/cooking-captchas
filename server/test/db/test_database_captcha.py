from datetime import datetime, timedelta
from typing import Dict, Generator
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from server.database.core import get_db
from server.main import app
from server.database import models
from server.database.captcha_helper import find_captcha, create_captcha, update_captcha
from server.database.schemas import CreateCaptcha, UpdateCaptcha

client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
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
        models.DBCaptcha(id=42, value="HELLO", is_used=True, created_at=datetime.now() - timedelta(days=1)),
        models.DBCaptcha(id=77, value="WORLD", is_used=False, created_at=datetime.now() - timedelta(days=1)),
    ]
    session.add_all(captchas)
    session.commit()
    yield {captcha.id: captcha for captcha in captchas}
    session.expunge_all()


@pytest.mark.parametrize(
    "captcha_id",
    [(1), (42), (77)],
)
def test_find_captcha(session, simple_captchas, captcha_id):
    db_captcha = find_captcha(session, captcha_id)
    original_captcha = simple_captchas[captcha_id]
    assert db_captcha.id == original_captcha.id
    assert db_captcha.value == original_captcha.value
    assert db_captcha.is_used == original_captcha.is_used
    assert db_captcha.created_at == original_captcha.created_at


@pytest.mark.parametrize(
    "value",
    [("ALPHA"), ("BETA"), ("GAMMA")],
)
def test_create_captcha(session, value):
    db_captcha = create_captcha(session, CreateCaptcha(value=value))
    assert db_captcha.id == 1
    assert db_captcha.value == value
    assert db_captcha.is_used is False
    assert db_captcha.created_at is not None
    selected_captcha = session.query(models.DBCaptcha).filter(models.DBCaptcha.id == 1).first()
    assert selected_captcha.id == db_captcha.id
    assert selected_captcha.value == db_captcha.value
    assert selected_captcha.is_used == db_captcha.is_used
    assert selected_captcha.created_at == db_captcha.created_at
    captcha_count = session.query(models.DBCaptcha).filter(models.DBCaptcha.id == 1).count()
    assert captcha_count == 1


@pytest.mark.parametrize(
    "captcha_id, update_payload",
    [(1, UpdateCaptcha(is_used=True))],
)
def test_update_captcha(session, simple_captchas, captcha_id, update_payload):
    db_captcha = simple_captchas[captcha_id]
    updated_captcha = update_captcha(session, db_captcha.id, update_payload)
    assert updated_captcha.is_used == update_payload.is_used
    assert updated_captcha.id == db_captcha.id
    assert updated_captcha.value == db_captcha.value
    assert updated_captcha.created_at == db_captcha.created_at
    selected_captcha = session.query(models.DBCaptcha).filter(models.DBCaptcha.id == captcha_id).first()
    assert selected_captcha.is_used == update_payload.is_used
    assert selected_captcha.id == db_captcha.id
    assert selected_captcha.value == db_captcha.value
    assert selected_captcha.created_at == db_captcha.created_at
    captcha_count = session.query(models.DBCaptcha).filter(models.DBCaptcha.id == captcha_id).count()
    assert captcha_count == 1
