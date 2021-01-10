from http import HTTPStatus
from datetime import datetime
from typing import List, Dict

import pytest
import json

from app.models.transactions import Transaction
from app.models.users import User

from app.data_types import Transaction as dt_Transaction

CURR_MONTH = datetime.now().month
CURR_YEAR = datetime.now().year

@pytest.fixture
def load_default(db):
    user1 = User(
            id=0,
            first_name="James",
            last_name="Jones",
            email="jons@test.com",
            password="123456",
            is_active=True,
            created_on=datetime.now(),
        )
    user2 = User(
        id=1,
        first_name="Jack",
        last_name="Jones",
        email="jons@test.com",
        password="123456",
        is_active=True,
        created_on=datetime.now(),
    )
    db.add(user1)
    db.add(user2)
    db.commit()

    transaction: Transaction = Transaction(
        id = 1,
        transaction_date = datetime(2020,9,1,0,0,0,0),
        transaction_type = "Deposit", 
        description = "Init",
        charge = 0.00,
        deposit = 100.00, 
        notes = "Depo", 
        createdOn = datetime(2020,9,1,0,0,0,0),
        user_id = 1
    )


    transaction2: Transaction = Transaction(
        id = 2,
        transaction_date = datetime(CURR_YEAR,CURR_MONTH,1,0,0,0,0),
        transaction_type = "Deposit", 
        description = "Init",
        charge = 0.00,
        deposit = 100.00, 
        notes = "Depo", 
        createdOn = datetime(CURR_YEAR,CURR_MONTH,1,0,0,0,0),
        user_id = 1
    )

    db.add(transaction)
    db.add(transaction2)
    db.commit()

def test_create_transaction(load_default, test_client):
    transaction: Transaction = Transaction(
        id = 3,
        transaction_date = datetime.now(),
        transaction_type = "Deposit", 
        description = "Init",
        charge = 0.00,
        deposit = 100.00, 
        notes = "Depo", 
        createdOn = datetime.now(),
        user_id = 1
    )
    response = test_client.post("/transactions/", json=json.loads(dt_Transaction.from_orm(transaction).json()))
    assert response.status_code == HTTPStatus.CREATED

    response = test_client.get("/transactions/3")
    assert response.status_code == HTTPStatus.OK

    data: Transaction = Transaction(**response.json())
    assert data.transaction_type == "Deposit"

def test_get_transactions_year_month(load_default, test_client):
    response = test_client.get(f"/transactions/{CURR_YEAR}/{CURR_MONTH}")
    assert response.status_code == HTTPStatus.OK

    data:List[Transaction] = response.json()
    assert len(data) == 1

    transaction:Transaction = Transaction(**data[0])
    assert transaction.deposit == 100.00


def test_get_transactions_balance_by_year_month_user(load_default, test_client):
    transaction: Transaction = Transaction(
        id = 3,
        transaction_date = datetime.now(),
        transaction_type = "Deposit", 
        description = "Init",
        charge = 0.00,
        deposit = 100.00, 
        notes = "Depo", 
        createdOn = datetime.now(),
        user_id = 1
    )
    response = test_client.post("/transactions/", json=json.loads(dt_Transaction.from_orm(transaction).json()))
    assert response.status_code == HTTPStatus.CREATED
    
    response = test_client.get(f"/transactions/balance/{CURR_YEAR}/{CURR_MONTH}", headers = {"user_id": "1"})
    assert response.status_code == HTTPStatus.OK

    data:Dict[float, float] = response.json()
    assert float(data["charge"]) == 0.00
    assert float(data["deposit"]) == 200.00


def test_get_transactions_balance_by_year_month_user_no_data(load_default, test_client):
    transaction: Transaction = Transaction(
        id = 3,
        transaction_date = datetime.now(),
        transaction_type = "Deposit", 
        description = "Init",
        charge = 0.00,
        deposit = 100.00, 
        notes = "Depo", 
        createdOn = datetime.now(),
        user_id = 1
    )
    response = test_client.post("/transactions/", json=json.loads(dt_Transaction.from_orm(transaction).json()))
    assert response.status_code == HTTPStatus.CREATED
    
    response = test_client.get(f"/transactions/balance/{CURR_YEAR}/{CURR_MONTH}", headers = {"user_id": "5"})
    assert response.status_code == HTTPStatus.OK

    data:Dict[float, float] = response.json()
    assert float(data["charge"]) == 0.00
    assert float(data["deposit"]) == 0.00

