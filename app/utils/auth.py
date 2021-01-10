from typing import List, Dict, Optional
from datetime import datetime, timedelta

from app.dependancies import  pwd_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, jwt


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)