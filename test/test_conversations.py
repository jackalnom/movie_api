from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_add_conversation_422_1():
    # case of char_ids not existing
    testJSON = {
                "character_1_id": 902100,
                "character_2_id": 902300,
                "lines": [
                    {
                        "character_id": 902100,
                        "line_text": "test"
                    }
                ]
            }
    response = client.post("/movies/615/conversations/", data=testJSON)
    assert response.status_code == 422


def test_add_conversation_422_2():
    # case where char_ids are from different movie
    testJSON = {
                "character_1_id": 1,
                "character_2_id": 0,
                "lines": [
                    {
                        "character_id": 0,
                        "line_text": "test"
                    }
                ]
            }
    response = client.post("/movies/615/conversations/", data=testJSON)
    assert response.status_code == 422


def test_add_conversation_422_3():
    # case where char_ids are the same
    testJSON = {
                "character_1_id": 9021,
                "character_2_id": 9021,
                "lines": [
                    {
                        "character_id": 9021,
                        "line_text": "test"
                    }
                ]
            }
    response = client.post("/movies/615/conversations/", data=testJSON)
    assert response.status_code == 422


def test_add_conversation_422_4():
    # case where a line uses a char_id not specified in the convo char_ids
    testJSON = {
                "character_1_id": 9021,
                "character_2_id": 9023,
                "lines": [
                    {
                        "character_id": 1,
                        "line_text": "test"
                    }
                ]
            }
    response = client.post("/movies/615/conversations/", data=testJSON)
    assert response.status_code == 422

    # manually tested success and failure cases as well
    # because it didn't like my testJSON formatting and couldn't figure out why
