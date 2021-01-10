from sqlalchemy import Boolean, Column, Integer, String, Date
from app.dependancies import Base

from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    created_on = Column(Date, default=datetime.now())
