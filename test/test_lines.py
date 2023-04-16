from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_line():
    response = client.get("/lines/60")
    assert response.status_code == 200

    with open("test/lines/60.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_404():
    response = client.get("/lines/1")
    assert response.status_code == 404
