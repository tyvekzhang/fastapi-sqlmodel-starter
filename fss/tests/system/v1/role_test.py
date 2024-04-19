import pytest
from fastapi.testclient import TestClient

from fss.common.config import configs
from fss.common.security.security import get_user_id
from fss.starter.server import app

client = TestClient(app)


def test_user_register():
    user_data = {
        "username": "example_user",
        "password": "example_password",
        "nickname": "Example Nickname",
    }
    response = client.post(f"{configs.api_version}/user/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["code"] == 0


@pytest.fixture(scope="class")
def login():
    response = client.post(
        f"{configs.api_version}/user/login",
        data={"username": "example_user", "password": "example_password"},
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


def test_list_ordered_role(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/role/listOrdered", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_get_role(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/role/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_remove_role_by_ids(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post(
        f"{configs.api_version}/role/roles", data="[1, 2, 3]", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_page_ordered_role(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/role/pageOrdered", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_remove_user(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"{configs.api_version}/user/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
