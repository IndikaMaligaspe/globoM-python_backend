import os
import hashlib

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from app.config import Config
from app.models import users
from app.database import get_db

DB_URL = os.environ["SQLALCHEMY_DATABASE_URI"]
SALT = os.environ["SALT"]


def get_conn():
    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db

if __name__ == "__main__":
    db:Session = get_conn()
    user: users.User = users.User(
        id=1,
        first_name="admin",
        last_name="",
        email="test@test.com",
        password = hashlib.pbkdf2_hmac('sha256', "123456".encode('utf-8'), SALT, 100000),
        is_active=True,
        created_on=datetime.now(),
    )
    db.add(user)
    db.commit()