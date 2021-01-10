from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc
from http import HTTPStatus
from datetime import datetime, timedelta


from app.database import get_db

from app.dependancies import oauth2_bearer

from app.data_queries import (
    get_users as dq_get_users,
    get_user_by_id as dq_get_user_by_id,
    get_user_by_email as dq_get_user_by_email,
    create_user as dq_create_user,
    update_user as dq_update_user,
)

from app.data_types import (
    User,
)

from app.utils import auth as auth_utils

router = APIRouter(
    dependencies=[Depends(get_db)],
)



@router.get("/users/", tags=["users"])
async def get_users(db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> List[User]:
    results: List[User] = await dq_get_users(db)
    return results


@router.get("/users/{id}", tags=["users"])
async def get_user_by_id(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> Optional[User]:
    result: User = await dq_get_user_by_id(db, id)
    if not result:
        return HTTPStatus.NOT_FOUND
    return User.from_orm(result)


@router.get("/users/email/{email}", tags=["users"])
async def get_user_by_email(email: str, db: Session = Depends(get_db)) -> Optional[User]:
    print(f"email - {email}")
    result: User = await dq_get_user_by_email(db, email)
    if not result:
        return HTTPStatus.NOT_FOUND
    return User.from_orm(result)


@router.post("/users/", status_code=201, tags=["users"])
async def create_user(body: User, db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)):
    if not body:
        return HTTPStatus.BAD_REQUEST
    try:
        body.password = auth_utils.get_hash_password(body.password)
        await dq_create_user(db, body)
    except exc.IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="ID Already exists")
    return HTTPStatus.CREATED


@router.patch("/users/{id}", response_model=User, tags=["users"])
async def update_user(body: Dict, id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)):
    if not body:
        return HTTPStatus.BAD_REQUEST
    try:
        response: User = await dq_update_user(db, body, id)
        return response
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.args)
