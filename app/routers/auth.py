from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc
from http import HTTPStatus
from datetime import datetime, timedelta


from app.database import get_db

from app.dependancies import oauth2_bearer, oauth2_request_form, pwd_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, jwt

from app.data_queries import (
    get_user_by_email as dq_get_user_by_email,

)

from app.data_types import (
    LoginUser,
    UserInDB,
    TokenData,
    Token,
    User,
)

from app.utils import auth as auth_utils

router = APIRouter(
    dependencies=[Depends(get_db)],
)


def verify_password(plain_password, hashed_password):
    return auth_utils.verify_password(plain_password, hashed_password)


def get_hash_password(password: str):
    return auth_utils.get_hash_password(password)


async def get_user(db, email: str) -> LoginUser:
    result: User = await dq_get_user_by_email(db, email)
    if result:
        return UserInDB(
          user_id = result.id,
          email=result.email,
          full_name = result.first_name.join(result.last_name),
          dissabled= False,
          hashed_password = result.password
        )

async def authenticate_user(db: Session, email: str, password: str) ->LoginUser:
    user:LoginUser = await get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)):
    credential_exception =  HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except Exception as e:
        raise credential_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(current_user: LoginUser = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/auth/token", tags=["auth"])
async def login_for_access_token(db: Session = Depends(get_db), form_data: oauth2_request_form = Depends()):
    print(f"inside login for access...")
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user":user}


@router.get("/auth/me", tags=["auth"],  response_model=LoginUser) 
async def read_users_me(current_user: LoginUser = Depends(get_current_user)) ->  LoginUser:
    return current_user

