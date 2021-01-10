import os

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.main import app
from app.config import Config
from app.database import get_db
from sqlalchemy.orm import sessionmaker
from app.dependancies import oauth2_bearer

# from app import db as _db

TEST_DB_URL = os.environ["SQLALCHEMY_TEST_DATABASE_URI"]

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_override_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def get_override_token():
    return "1111"


@pytest.fixture
def config(monkeypatch):
    environment = {"SQLALCHEMY_DATABASE_URI": TEST_DB_URL}

    for key, value in environment.items():
        monkeypatch.setenv(key, value)
    return Config.from_env()


@pytest.fixture
def alembic_engine():
    return create_engine(TEST_DB_URL)


@pytest.fixture
def alembic_config():
    return {
        "script_location": "alembic",
    }


@pytest.fixture
def test_client(loop, config):
    app.dependency_overrides[get_db] = get_override_db
    app.dependency_overrides[oauth2_bearer] = get_override_token

    client = TestClient(app)
    return client


@pytest.fixture
async def db(loop, config, alembic_runner):
    _db = TestingSessionLocal()
    try:
        alembic_runner.migrate_up_to("head")
        yield _db
    finally:
        alembic_runner.migrate_down_to("base")
