from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from collections import Counter

router = APIRouter()

@router.get("/lines/{id}", tags=["lines"])
def get_line(id: str):
    """
    This endpoint returns a single line by its identifier. For each line
    it returns:
    * `line_id`: the internal id of the line. Can be used to query the 
       `/lines/{line_id}` endpoint. 
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `movie_id`: the internal id of the movie.
    * `conversation_id`: the internal id of the conversation
    * `line_text`: the text of the line 
    """

    # get line
    try:
        line = db.lines[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Line not found")

    result = {
        "line_id": int(id),
        "character_id": int(line["character_id"]),
        "movie_id": int(line["movie_id"]),
        "conversation_id": int(line["conversation_id"]),
        "line_text": line["line_text"] or None
    }
    return result



