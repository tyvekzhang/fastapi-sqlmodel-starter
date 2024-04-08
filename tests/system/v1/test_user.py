from fastapi.testclient import TestClient

from fss.common.config import configs
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
