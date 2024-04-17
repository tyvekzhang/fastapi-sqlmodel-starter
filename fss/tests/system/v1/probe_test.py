from fastapi.testclient import TestClient

from fss.common.config import configs
from fss.starter.server import app

client = TestClient(app)


def test_probe_liveness():
    response = client.get(f"{configs.api_version}/probe/liveness")
    assert response.status_code == 200
    assert response.json() == {"code": 0, "msg": "hi"}


def test_probe_readiness():
    response = client.get(f"{configs.api_version}/probe/readiness")
    assert response.status_code == 200
    assert response.json() == {"code": 0, "msg": "hello"}
