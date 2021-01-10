from http import HTTPStatus
from datetime import datetime
from typing import List, Dict

import pytest
import json

from app.models import users
from app.data_types import User

@pytest.fixture
def load_default(db):
    user1 = users.User(
        id=0,
        first_name="James",
        last_name="Jones",
        email="jons@test.com",
        password="123456",
        is_active=True,
        created_on=datetime.now(),
    )
    user2 = users.User(
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


def test_get_users(load_default, test_client):
    response = test_client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    data: List[User] = [user for user in response.json()]
    assert len(data) == 2
    assert data[0]["email"] == "jons@test.com"


def test_get_user_by_id(load_default, test_client):
    response = test_client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    user: User = User(**response.json())
    user.email == "jons@test.com"


def test_create_user(load_default, test_client):
    response = test_client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    data: List[User] = [user for user in response.json()]
    _id: int = len(data) + 1
    user: User = User(
        id=_id,
        first_name="Jane",
        last_name="Smith",
        email="jumbo@test.com",
        password="123456",
        is_active=True,
        created_on=datetime.now(),
    )
    response = test_client.post("/users/", json=json.loads(user.json()))
    assert response.status_code == HTTPStatus.CREATED

    response = test_client.get(f"/users/{_id}")
    assert response.status_code == HTTPStatus.OK
    user: User = User(**response.json())
    user.email == "jumbo@test.com"


def test_create_user_duplicate_entry(load_default, test_client):
    response = test_client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    data: List[User] = [user for user in response.json()]
    _id: int = len(data) + 1
    user: User = User(
        id=_id,
        first_name="Jane",
        last_name="Smith",
        email="jumbo@test.com",
        password="123456",
        is_active=True,
        created_on=datetime.now(),
    )
    response = test_client.post("/users/", json=json.loads(user.json()))
    assert response.status_code == HTTPStatus.CREATED

    user: User = User(
        id=_id,
        first_name="Jane",
        last_name="Smith",
        email="jumbo@test.com",
        password="123456",
        is_active=True,
        created_on=datetime.now(),
    )
    response = test_client.post("/users/", json=json.loads(user.json()))
    assert response.status_code == HTTPStatus.CONFLICT


def test_update_user(load_default, test_client):
    response = test_client.patch("/users/1", json={"email": "jumbo@test.com"})
    assert response.status_code == HTTPStatus.OK

    user: User = User(**response.json())
    assert user.email == "jumbo@test.com"


def test_update_user_with_no_change(load_default, test_client):
    response = test_client.patch("/users/1", json={"email": "jons@test.com"})
    data: Dict = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["detail"][0] == "Content not changed"
