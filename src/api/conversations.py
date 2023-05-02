from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
from src.datatypes import Conversation, Line
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
    with db.engine.begin() as conn:
        # Insert conversation into conversations table
        conversation_values = {"movie_id": movie_id,
                               "character1_id": conversation.character_1_id,
                               "character2_id": conversation.character_2_id}
        conversation_stmt = db.conversations.insert().values(conversation_values)
        conversation_result = conn.execute(conversation_stmt)

        # Get conversation_id from the result of the previous insert
        conversation_id = conversation_result.inserted_primary_key[0]

        # Insert lines into lines table
        for line in conversation.lines:
            line_values = {"conversation_id": conversation_id,
                           "character_id": line.character_id,
                           "line_text": line.line_text}
            line_stmt = db.lines.insert().values(line_values)
            conn.execute(line_stmt)
    return conversation_id
    # try:
    #     char1 = db.characters[conversation.character_1_id]
    #     char2 = db.characters[conversation.character_2_id]
    # except KeyError:
    #     raise HTTPException(status_code=422, detail="Validation Error: 1+ given char_ids are invalid")
    # if char1.movie_id != movie_id or char2.movie_id != movie_id:
    #     raise HTTPException(status_code=422, detail="Validation Error: Invalid character for given movie")
    # if char1.id == char2.id:
    #     raise HTTPException(status_code=422, detail="Validation Error: Both characters in conversation have same ID")
    # for line in conversation.lines:
    #     if line.character_id != char1.id and line.character_id != char2.id:
    #         raise HTTPException(status_code=422, detail="Validation Error: char_id of a line was not specified in the "
    #                                                     "given conversation")
    # # Doing a second run through lines to assign IDs because I dont want incorrectly increment MaxID in db in the case
    # # that a line had Invalid Format. If I get here, all data is validated and I can add the lines and convo to the db
    # newConvoID = db.maxConvoID + 1
    # db.maxConvoID += 1
    # # adding to local database so it updates as soon as it's added
    # db.conversations[newConvoID] = Conversation(
    #                                 newConvoID,
    #                                 conversation.character_1_id,
    #                                 conversation.character_2_id,
    #                                 movie_id,
    #                                 len(conversation.lines),
    #                             )
    # # adding to supabase
    # db.convos.append({"conversation_id": newConvoID, "character1_id": conversation.character_1_id,
    #                   "character2_id": conversation.character_2_id, "movie_id": movie_id})
    # db.upload_new_conversations()
    # # onto lines
    # newLineSort = 1
    # for line in conversation.lines:
    #     # adding to local database so it updates as soon as it's added
    #     newLineID = db.maxLineID + 1
    #     db.maxLineID += 1
    #     db.lines[newLineID] = Line(
    #                             newLineID,
    #                             line.character_id,
    #                             movie_id,
    #                             newConvoID,
    #                             newLineSort,
    #                             line.line_text,
    #                         )
    #     # adding to supabase
    #     db.lin.append({"line_id": newLineID, "character_id": line.character_id, "movie_id": movie_id,
    #                    "conversation_id": newConvoID, "line_sort": newLineSort, "line_text": line.line_text})
    #     newLineSort += 1
    # db.upload_new_lines()
    # return newConvoID
