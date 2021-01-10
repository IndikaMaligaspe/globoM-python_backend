import os
from typing import TypeVar, Type, Any
from dataclasses import dataclass, fields

T = TypeVar("T", bound="EnvironMixin")


class EnvironMixin:
    @classmethod
    def from_env(cls: Type[T]) -> T:
        init_args = {}
        for field in fields(cls):
            if field.name in os.environ:
                value: Any = os.environ[field.name]
                init_args[field.name] = value
        return cls(**init_args)


@dataclass
class Config(EnvironMixin):
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_USER_NAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
