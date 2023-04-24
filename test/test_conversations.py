from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_add_conversation():
    conversation_data = {
        "character_1_id": 198,
        "character_2_id": 199,
        "lines": [
            {
                "character_id": 198,
                "line_text": "string"
            },
            {
                "character_id": 199,
                "line_text": "asdf"
            },
        ]
    }
    response = client.post("/movies/13/conversations/", json=conversation_data)
    assert response.status_code == 200

    line_response = client.get("/lines/?character_id=199&limit=100")
    assert line_response.status_code == 200

    found = False 
    for line in line_response.json()["lines"]:
        if line.get("line_text") == "asdf":
            found = True

    assert found == True 

def test_add_conversation2():
    conversation_data = {
        "character_1_id": 1326,
        "character_2_id": 1327,
        "lines": [
            {
                "character_id": 1326,
                "line_text": "string"
            },
            {
                "character_id": 1326,
                "line_text": "asdf"
            },
        ]
    }
    response = client.post("/movies/89/conversations/", json=conversation_data)
    assert response.status_code == 200

    line_response = client.get("/lines/?character_id=1326&limit=100")
    assert line_response.status_code == 200

    found = False 
    for line in line_response.json()["lines"]:
        if line.get("line_text") == "asdf":
            found = True

    assert found == True 

