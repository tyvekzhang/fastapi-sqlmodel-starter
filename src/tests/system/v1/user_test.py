import io

import pandas as pd
import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from fss.common.config import configs
from fss.common.util.security import get_user_id
from fss.starter.server import app
from fss.starter.system.schema.user_schema import UpdateUserCmd

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
    yield response.json()["access_token"], user_id


def test_user_login():
    response = client.post(
        f"{configs.api_version}/user/login",
        data={"username": "example_user", "password": "example_password"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_user_me():
    login_response = client.post(
        f"{configs.api_version}/user/login",
        data={"username": "example_user", "password": "example_password"},
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/user/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_update_user(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    updateUserCmd = UpdateUserCmd(id=f"{user_id}", nickname="example_nickname")
    response = client.put(
        f"{configs.api_version}/user",
        json=(updateUserCmd.model_dump()),
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_export_user_template(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/user/exportTemplate", headers=headers)
    assert response.status_code == 200


def test_export_user(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{configs.api_version}/user/export", headers=headers)
    assert response.status_code == 200


def test_import_user(login):
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
        f"{configs.api_version}/user/import",
        headers=headers,
        files={"file": (file.filename, file.file, file.content_type)},
    )
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_remove_user(login):
    access_token, user_id = login
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"{configs.api_version}/user/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
