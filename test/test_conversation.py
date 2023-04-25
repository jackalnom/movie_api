from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_add_conversation():
    # Test case 1: Valid conversation
    movie_id = 0
    conversation = {
        "character_1_id": 0,
        "character_2_id": 2,
        "lines": [
            {
                "character_id": 0,
                "line_text": "test"
            },
            {
                "character_id": 2,
                "line_text": "IM DONE"
            },
            {
                "character_id": 0,
                "line_text": "GOODNIGHT"
            }
        ]
    }
    response = client.post(f"/movies/{movie_id}/conversations/", json=conversation)
    assert response.status_code == 200

def test_add_conversation2():
    # Test case 2: invalid conversation (same character)
    movie_id = 0
    conversation = {
        "character_1_id": 0,
        "character_2_id": 0,
        "lines": [
            {
                "character_id": 0,
                "line_text": "test"
            },
            {
                "character_id": 2,
                "line_text": "IM DONE"
            },
            {
                "character_id": 0,
                "line_text": "GOODNIGHT"
            }
        ]
    }
    response = client.post(f"/movies/{movie_id}/conversations/", json=conversation)
    assert response.status_code == 404

    
