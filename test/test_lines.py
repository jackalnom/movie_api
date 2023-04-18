from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_line():
    response = client.get("/lines/49")
    assert response.status_code == 200

    with open("test/lines/49.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_character_lines():
    response = client.get("/character_lines/?character_name=Ben&movie_title=blue%20Velvet")
    assert response.status_code == 200

    with open("test/lines/ben_blue_velvet.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_convo_lines():
    response = client.get("/convo_lines/83073")
    assert response.status_code == 200

    with open("test/lines/83073.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_404_lines():
    response = client.get("/lines/48")
    assert response.status_code == 404

def test_404_character_lines():
    response = client.get("/character_lines/?character_name=Ben&movie_title=red%20Velvet")
    assert response.status_code == 404

def test_404_convo():
    response = client.get("/convo_lines/83074")
    assert response.status_code == 404