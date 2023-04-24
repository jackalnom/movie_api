from fastapi import APIRouter, HTTPException
from src import database as db
from src import datatypes as dt
from pydantic import BaseModel
from typing import List
from datetime import datetime
from random import randint



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
    

    # create new Conversation obj and upload
    new_convo_id = generate_new_number(db.conversations)
    new_convo = dt.Conversation(
        new_convo_id,
        conversation.character_1_id,
        conversation.character_1_id,
        movie_id,
        len(conversation.lines)
    )
    db.conversations[new_convo_id] = new_convo
    db.upload_new_conversation()

    # create new Line objs and upload
    line_sort = 0
    for line in conversation.lines:
        new_line_id = generate_new_number(db.lines)
        new_line = dt.Line(
            new_line_id,
            line.character_id,
            movie_id,
            new_convo_id,
            line_sort, 
            line.line_text
        )
        db.lines[new_line_id] = new_line
        db.upload_new_line()
        line_sort += 1

    return new_convo_id

def generate_new_number(d):
    while True:
        rand_int = randint(0, 100000)
        if rand_int not in d:
            return rand_int
        