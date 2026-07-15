from fastapi.testclient import TestClient

from db import get_db
from server import app
from tests.utils import override_get_db

client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db


def test_enemies_get():
    response = client.get("/enemies")
    assert response.status_code == 200
    enemies = response.json()
    assert len(enemies) == 4
