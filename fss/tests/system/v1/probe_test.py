import pytest
from fastapi.testclient import TestClient

from fss.common.config import configs


@pytest.fixture
def client():
    from fss.starter.server import app

    return TestClient(app)


@pytest.mark.parametrize(
    "endpoint,expected_json",
    [
        ("liveness", {"code": 0, "msg": "Hi"}),
        ("readiness", {"code": 0, "msg": "Hello"}),
    ],
)
def test_probe(client, endpoint, expected_json):
    response = client.get(f"{configs.api_version}/probe/{endpoint}")
    assert response.status_code == 200
    assert response.json() == expected_json
