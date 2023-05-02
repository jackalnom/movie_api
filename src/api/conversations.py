from fastapi import APIRouter, HTTPException
from src import database as db
from src import datatypes as dt
from pydantic import BaseModel
from typing import List
import sqlalchemy



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

    """
    Areas where the code will not function
    - multiple simultaneous calls to this endpoint 
        - could add to conversations csv and lines csv on Supabase 
            - possibly multiple instances of lines or conversations 
            with the same primary id (if there is reentrancy)
    - could fail to add the resource if there is a race condition with 
      another endpoint call that affects the data required for this call to succeed 
      (such as character data and line data)
    """

    with db.engine.connect() as conn:
        char1 = conn.execute(
            sqlalchemy.text("""SELECT * FROM characters WHERE characters.character_id = :x"""), 
            [{"x": conversation.character_1_id}]
        ).fetchone()  

        char2 = conn.execute(
            sqlalchemy.text("""SELECT * FROM characters WHERE characters.character_id = :x"""), 
            [{"x": conversation.character_2_id}]
        ).fetchone()    

        # --- ensure the request body
        # characters are part of the referenced movie 
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
            if (line.character_id != char1.character_id) and (line.character_id != char2.character_id):
                raise HTTPException(status_code=404, detail="a line referenced does not include either character in the conversation.")

        new_conv_id = conn.execute(
            sqlalchemy.text("""
            SELECT conversations.conversation_id
            FROM conversations
            ORDER BY conversation_id DESC
            LIMIT 1 
            """)
        ).fetchone().conversation_id + 1

        new_convo = {
            "conversation_id": new_conv_id,
            "character1_id": char1.character_id,
            "character2_id": char2.character_id,
            "movie_id": movie_id
        }
            
        conn.execute(db.conversations.insert().values(**new_convo))
        

        new_line_id = conn.execute(
            sqlalchemy.text("""
            SELECT lines.line_id
            FROM lines
            ORDER BY line_id DESC
            LIMIT 1 
            """)
        ).fetchone().line_id + 1

        # create new Line objs and upload
        line_sort = 0
        for line in conversation.lines:
            new_line = {
                "line_id": new_line_id,
                "character_id": conversation.character_1_id,
                "movie_id": movie_id,
                "conversation_id": line.character_id,
                "line_sort": line_sort,
                "line_text": line.line_text
            }
            new_line_id += 1
            line_sort += 1
            conn.execute(db.lines.insert().values(**new_line))

        conn.commit()

        return new_conv_id
    