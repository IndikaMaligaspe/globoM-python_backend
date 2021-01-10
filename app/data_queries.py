from typing import List, Dict, Optional
from app.models.users import User
from app.models.transactions import Transaction
from app.data_types import (
    User as dt_user, 
    Transaction as dt_Transacion,
)
from datetime import datetime
from sqlalchemy import and_


async def get_users(db) -> List[User]:
    user_list: List[User] = db.query(User).all()
    return user_list


async def get_user_by_id(db, id: int) -> Optional[User]:
    response: User = db.query(User).get(id)
    return response


async def get_user_by_email(db, email: str) -> User:
    response: User = db.query(User).filter(User.email == email).first()
    return response


async def create_user(db, user: dt_user):
    db_user: User = User(**user.dict())
    db.add(db_user)
    db.commit()


async def update_user(db, data: Dict, id: int) -> dt_user:
    db_user: User = db.query(User).get(id)
    user_dict: Dict = dt_user.from_orm(db_user).dict()
    new_data: bool = False
    for key, value in data.items():
        if user_dict[key] != value:
            new_data = True

    if not new_data:
        raise Exception("Content not changed")
    db.query(User).filter(User.id == id).update(data)
    db.commit()
    db.refresh(db_user)
    return dt_user.from_orm(db_user)

async def get_transaction(db, id:int) -> Transaction:
    transaction: Transaction = db.query(Transaction).get(id)
    return transaction

async def create_transaction(db, data: dt_Transacion):
    transaction: Transaction = Transaction(**data.dict())
    query:str = """
    SELECT MAX(id) as max_id
    FROM transactions     
    """
    max_id: int  = db.execute(query).fetchone().max_id
    transaction.id = max_id + 1
    db.add(transaction)
    db.commit()

async def get_transactions_by_year_month(db, year:int, month:int):
    start_date = datetime(year, month,1,0,0,0,0)
    if month==12:
        month=0
        year +=1
    end_date = datetime(year, month+1,1,0,0,0,0)
    transactions:List[Transaction] = db.query(Transaction).filter(and_(Transaction.transaction_date >= start_date, Transaction.transaction_date <= end_date)).all()
    return transactions


async def get_transaction_balance_by_year_month_user(db, year:int, month: int, user_id: int):
    start_date = datetime(year, month,1,0,0,0,0)
    if month==12:
        month=0
        year +=1
    end_date = datetime(year, month+1,1,0,0,0,0)

    query:str = """
    SELECT 
    SUM(charge) as "charge",
    SUM(deposit) as "deposit"
    FROM transactions
    WHERE 
    user_id = :user_id
    AND
    transaction_date >= :start_date
    AND
    transaction_date <= :end_date
    GROUP BY user_id
    """
    params = {"user_id":user_id, "start_date":start_date, "end_date": end_date}
    result = db.execute(query, params)
    record = result.fetchone()
    if not record:
        return {"charge": 0.00, "deposit": 0.00}    
    return {"charge": record.charge, "deposit":record.deposit}