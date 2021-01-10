from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict 
from http import HTTPStatus
from sqlalchemy.orm import Session


from app.database import get_db
from app.dependancies import oauth2_bearer

from app.data_types import (
    Transaction,
)

from app.data_queries import (
    get_transaction as dq_get_transaction,
    create_transaction as dq_create_transaction,
    get_transactions_by_year_month as dq_get_transactions_by_year_month,
    get_transaction_balance_by_year_month_user as dq_get_transaction_balance_by_year_month_user,
)

router = APIRouter(
    dependencies=[Depends(get_db)],
)


@router.get("/transactions/{id}", response_model=Transaction, tags=["Transaction"])
async def get_transaction(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> Transaction:
   result = await dq_get_transaction(db, id)
   if not result:
       raise HTTPException(HTTPStatus.NOT_FOUND, "No Records Found.")
   return Transaction.from_orm(result)


@router.get("/transactions/{year}/{month}", response_model=List[Transaction], tags=["Transaction"])
async def get_transactions_by_year_month(year: int, month: int, db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> Transaction:
    results: List[Transaction] = await dq_get_transactions_by_year_month(db, year, month)
    return [Transaction.from_orm(result) for result in results]


@router.get("/transactions/balance/{year}/{month}", response_model=Dict[str, str], tags=["Transaction"])
async def get_transactions_balance_by_year_month_user(year: int, month: int, request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> Transaction:
    user_id = request.headers["user_id"]
    if not user_id:
        return HTTPStatus.BAD_REQUEST
    result: Dict[float, float] = await dq_get_transaction_balance_by_year_month_user(db, year, month, user_id)
    return result


@router.post("/transactions/", status_code=HTTPStatus.CREATED, tags=["Transaction"])
async def create_transaction(body: Transaction , db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)):
   await dq_create_transaction(db, body)
   return HTTPStatus.CREATED
