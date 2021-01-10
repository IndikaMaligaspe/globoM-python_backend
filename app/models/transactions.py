from sqlalchemy import Column, Date, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.dependancies import Base

from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    charge = Column(Numeric, default=0)
    deposit = Column(Numeric, default=0)
    notes = Column(String)
    createdOn = Column(Date, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    transaction_user = relationship("User", foreign_keys=[user_id])
