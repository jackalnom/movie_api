from fastapi import APIRouter, HTTPException
from src import database as db
from src import datatypes as dt
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

    # --- ensure the request body
    # characters are part of the referenced movie 
    c1_id, c2_id = conversation.character_1_id, conversation.character_2_id
    char1, char2 = db.characters.get(c1_id), db.characters.get(c2_id)
    if not char1:
        raise HTTPException(status_code=404, detail="character 1 not found.")
    if not char2:
        raise HTTPException(status_code=404, detail="character 2 not found.")
    if (char1.movie_id != movie_id) or (char2.movie_id != movie_id):
        raise HTTPException(status_code=404, detail="characters in request body are not part of referenced movie.")

    # characters are not the same 
    if char1 == char2:
        raise HTTPException(status_code=404, detail="the two characters in request body are the same.")
    
    # lines match the characters involved 
    for line in conversation.lines:
        if (line.character_id != c1_id) and (line.character_id != c2_id):
            raise HTTPException(status_code=404, detail="a line referenced does not include either character in the conversation.")

    # fake_convo = {
    #     "conversation_id": 100000,
    #     "character1_id": 0,
    #     "character2_id": 1,
    #     "movie_id": 0
    # }


    # create Conversation obj and append to locally stored version of
    fake_convo = dt.Conversation(
        100000,
        0,
        1,
        0,
        0
    )
    db.conversations[100000] = fake_convo

    print(fake_convo)
    print(db.conversations[100000])
    db.upload_new_conversation()
    print("UPLOADED!")

    
    return
