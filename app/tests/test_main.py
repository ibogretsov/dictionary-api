from fastapi import status
from fastapi.testclient import TestClient


def test_healthcheck(client: TestClient):
    resp = client.get('/')
    assert resp.status_code == status.HTTP_200_OK
