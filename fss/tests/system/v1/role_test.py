import pytest
from fastapi.testclient import TestClient

from fss.common.config import configs
from fss.common.security.security import get_user_id
from fss.starter.server import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "endpoint, test_data, expected_status_code, expected_code",
    [
        (
            "register",
            {
                "username": "example_user",
                "password": "example_password",
                "nickname": "Example Nickname",
            },
            200,
            0,
        ),
    ],
)
def test_user_register(
    client, endpoint, test_data, expected_status_code, expected_code
):
    response = client.post(f"{configs.api_version}/user/{endpoint}", json=test_data)
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.fixture
def login(client):
    endpoint, test_data, expected_status_code, expected_token_type = (
        "login",
        {
            "username": "example_user",
            "password": "example_password",
        },
        200,
        "bearer",
    )
    response = client.post(
        f"{configs.api_version}/user/{endpoint}",
        data=test_data,
    )
    assert response.status_code == expected_status_code
    assert response.json()["token_type"] == expected_token_type
    access_token = response.json()["access_token"]
    user_id = get_user_id(access_token)
    yield access_token, user_id


@pytest.mark.parametrize(
    "endpoint, test_data, expected_status_code, expected_code",
    [
        (
            "role",
            {
                "id": 304456628861931520,
                "name": "example_role",
                "sort": 1,
                "remark": "Example remark",
            },
            200,
            0,
        ),
    ],
)
def test_create_role(
    login, client, endpoint, test_data, expected_status_code, expected_code
):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post(
        f"{configs.api_version}/{endpoint}", json=test_data, headers=headers
    )
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "endpoint, expected_status_code, expected_code",
    [
        ("rolesOrdered", 200, 0),
    ],
)
def test_list_ordered_role(
    login, client, endpoint, expected_status_code, expected_code
):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/role/{endpoint}", headers=headers)
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "user_id, expected_status_code, expected_code",
    [
        (1, 200, 0),
    ],
)
def test_get_role(login, client, user_id, expected_status_code, expected_code):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/role/{user_id}", headers=headers)
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "endpoint, test_dada, expected_status_code, expected_code",
    [
        ("roles", {"role_ids": [304456628861931520]}, 200, 0),
        ("roles", {"role_ids": [1]}, 200, 400),
    ],
)
def test_remove_role_by_ids(
    login, client, endpoint, test_dada, expected_status_code, expected_code
):
    access_token, user_id = login
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = client.post(
        f"{configs.api_version}/role/{endpoint}", json=test_dada, headers=headers
    )
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "expected_status_code, expected_code",
    [
        (200, 0),
    ],
)
def test_remove_user(login, client, expected_status_code, expected_code):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"{configs.api_version}/user/{user_id}", headers=headers)
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code
