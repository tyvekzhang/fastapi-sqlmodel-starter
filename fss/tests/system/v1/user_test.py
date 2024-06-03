import io

import pandas as pd
import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from fss.common.config import configs
from fss.common.security.security import get_user_id
from fss.starter.server import app
from fss.starter.system.schema.user_schema import UpdateUserCmd


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
        (
            "register",
            {
                "username": "example_user",
                "password": "example_password",
                "nickname": "Example Nickname",
            },
            200,
            100,
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
    "endpoint, test_data, expected_status_code",
    [
        (
            "login",
            {
                "username": "example_user",
                "password": "example_password_error",
            },
            401,
        ),
        (
            "login",
            {
                "username": "example_user_error",
                "password": "example_password_error",
            },
            401,
        ),
    ],
)
def test_user_login_error(client, endpoint, test_data, expected_status_code):
    response = client.post(
        f"{configs.api_version}/user/{endpoint}",
        data=test_data,
    )
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "endpoint, expected_status_code, expected_code",
    [
        (
            "me",
            200,
            0,
        ),
    ],
)
def test_user_me(login, client, endpoint, expected_status_code, expected_code):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/user/{endpoint}", headers=headers)
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "test_data, expected_status_code, expected_code",
    [
        (
            {
                "nickname": "example_nickname",
            },
            200,
            0,
        ),
    ],
)
def test_update_user(login, client, test_data, expected_status_code, expected_code):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    updateUserCmd = UpdateUserCmd(id=f"{user_id}", nickname=test_data["nickname"])
    response = client.put(
        f"{configs.api_version}/user",
        json=(updateUserCmd.model_dump()),
        headers=headers,
    )
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "endpoint, expected_status_code",
    [
        (
            "exportTemplate",
            200,
        ),
    ],
)
def test_export_user_template(login, client, endpoint, expected_status_code):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/user/{endpoint}", headers=headers)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "endpoint, expected_status_code",
    [
        (
            "export",
            200,
        ),
    ],
)
def test_export_user(login, client, endpoint, expected_status_code):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/user/{endpoint}", headers=headers)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "endpoint, expected_status_code, expected_code",
    [
        ("import", 200, 0),
    ],
)
def test_import_user(login, client, endpoint, expected_status_code, expected_code):
    access_token, user_id = login
    headers = {
        "Authorization": f"Bearer {access_token}",
        "content_type": "multipart/form-data",
    }
    df = pd.DataFrame(
        {
            "username": ["example_user_2"],
            "password": ["password"],
            "nickname": ["nickname"],
        }
    )
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    file = UploadFile(filename="test_users.xlsx", file=buffer)

    response = client.post(
        f"{configs.api_version}/user/{endpoint}",
        headers=headers,
        files={"file": (file.filename, file.file, file.content_type)},
    )
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "endpoint, expected_status_code, expected_code",
    [
        ("import", 200, 100),
    ],
)
def test_import_user_error(
    login, client, endpoint, expected_status_code, expected_code
):
    access_token, user_id = login
    headers = {
        "Authorization": f"Bearer {access_token}",
        "content_type": "multipart/form-data",
    }
    df = pd.DataFrame(
        {
            "username": ["example_user_2"],
            "password": ["password"],
            "nickname": ["nickname"],
        },
        {
            "username": ["example_user_2"],
            "password": ["password"],
            "nickname": ["nickname"],
        },
    )
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    file = UploadFile(filename="test_users.xlsx", file=buffer)

    response = client.post(
        f"{configs.api_version}/user/{endpoint}",
        headers=headers,
        files={"file": (file.filename, file.file, file.content_type)},
    )
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "endpoint, expected_status_code, expected_code",
    [
        ("list", 200, 0),
    ],
)
def test_list_user(login, client, endpoint, expected_status_code, expected_code):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/user/{endpoint}", headers=headers)
    assert response.status_code == expected_status_code
    assert response.json()["code"] == expected_code


@pytest.mark.parametrize(
    "endpoint, test_data, expected_status_code, expected_code",
    [
        ("roles", "[1, 2, 3]", 200, 0),
    ],
)
def test_user_roles(
    login, client, endpoint, test_data, expected_status_code, expected_code
):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post(
        f"{configs.api_version}/user/{user_id}/{endpoint}",
        content=test_data,
        headers=headers,
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

    response = client.post(
        f"{configs.api_version}/user/login",
        data={"username": "example_user_2", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    access_token = response.json()["access_token"]
    user_id = get_user_id(access_token)
    response = client.delete(f"{configs.api_version}/user/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
