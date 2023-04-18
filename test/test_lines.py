from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_lines_movie():
    response = client.get("/lines/movie/369")
    assert response.status_code == 200

    with open("test/linesAndConvos/test1.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_lines_character():
    response = client.get("/lines/character/?character=ja&limit=7&offset=2")
    assert response.status_code == 200

    with open("test/linesAndConvos/test2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_line_id():
    response = client.get(
        "/lines/49"
    )
    assert response.status_code == 200

    with open(
        "test/linesAndConvos/test3.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)


def test_404():
    response = client.get("/lines/1")
    assert response.status_code == 404
