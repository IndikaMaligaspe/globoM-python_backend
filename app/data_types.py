from typing import Optional

from datetime import date
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool
    created_on: date

    class Config:
        orm_mode = True

class Transaction(BaseModel):
    id: Optional[int]
    transaction_date: date
    transaction_type: str
    description: str
    charge: float = 0
    deposit: float = 0
    notes: str
    createdOn: date
    user_id: int

    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    user_id: Optional[int]
    email: Optional[str] = None
    full_name: Optional[str] = None
    dissabled: Optional[bool] = None


class UserInDB(LoginUser):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

