from fastapi.testclient import TestClient
from src.api.server import app
import json

client = TestClient(app)

def test_get_character():
    response = client.get("/characters/7421")
    assert response.status_code == 200

    with open("test/characters/7421.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_characters():
    response = client.get("/characters/")
    assert response.status_code == 200

    with open("test/characters/root.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_sort_filter():
    response = client.get(
        "/characters/?name=amy&limit=50&offset=0&sort=number_of_lines"
    )
    assert response.status_code == 200

    with open(
        "test/characters/characters-name=amy&limit=50&offset=0&sort=number_of_lines.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)

def test_404():
    response = client.get("/characters/400")
    assert response.status_code == 404

# additional test cases
def test_get_char1001():
    response = client.get("/characters/1001")
    assert response.status_code == 200

    with open("test/characters/1001.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_offset_and_sort():
    response = client.get(
        "/characters/?name=t&limit=50&offset=36&sort=movie"
    )
    assert response.status_code == 200

    with open(
        "test/characters/test_offset_and_sort.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)
