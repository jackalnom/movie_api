from fastapi import APIRouter, HTTPException
from src import database as db
from src.datatypes import Line
from pydantic import BaseModel
from typing import List
from datetime import datetime


# FastAPI is inferring what the request body should look like
# based on the following two classes.
class LinesJson(BaseModel):
    character_id: int
    line_text: str


class ConversationJson(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[LinesJson]


router = APIRouter()

def check_json(movie_id : int, conversation : ConversationJson):
    if db.characters[conversation.character_1_id].movie_id != movie_id:
        return False
    if db.characters[conversation.character_2_id].movie_id != movie_id:
        return False
    if conversation.character_1_id == conversation.character_2_id:
        return False
    for line in conversation.lines:
        if (line.character_id != conversation.character_1_id and
        line.character_id != conversation.character_2_id):
            return False
    return True

@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: ConversationJson):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.
    """

    # the two test cases are found in tests/test_conversation.py
    # I think overall the functionality of the post method is pretty solid, the only
    # functionality I would maybe like to add would be writing back to a previous conversation and including
    # maybe some additional lines. The check_json() function above I think does a pretty good of checking
    # what needs to be check in the spec.

    if check_json(movie_id, conversation):
        pass
    else:
        raise HTTPException(status_code=404, detail = "invalid conversation")
    
    convo_id = max(db.conversations.keys()) + 1
    line_id = max(db.lines.keys()) + 1

    i = 0
    while i < len(conversation.lines):
        line = Line(
            id = line_id + i,
            c_id = conversation.lines[i].character_id,
            movie_id = movie_id,
            conv_id = convo_id,
            line_sort = i + 1,
            line_text = conversation.lines[i].line_text       
        )
        db.lines[line_id + i] = line
        i += 1
        
    json = {
        "conversation_id" : convo_id,
        "character1_id" : conversation.character_1_id,
        "character2_id" : conversation.character_2_id,
        "movie_id" : movie_id
    }

    db.conversations[convo_id] = json
