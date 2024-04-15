import pytest
from fastapi.testclient import TestClient

from fss.common.config import configs
from fss.common.util.security import get_user_id
from fss.starter.server import app

client = TestClient(app)


@pytest.fixture(scope="class")
def login():
    response = client.post(
        f"{configs.api_version}/user/login",
        data={"username": "example_user_2", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    access_token = response.json()["access_token"]
    user_id = get_user_id(access_token)
    yield access_token, user_id


def test_create_role(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    role_data = {
        "name": "example_role",
        "sort": 1,
        "remark": "Example remark",
    }
    response = client.post(
        f"{configs.api_version}/role", json=role_data, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_remove_user(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"{configs.api_version}/user/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
