from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()

# Assignment 2

# Create lines.py and create three new calls that leverages at least the lines and conversations data.
# One of the calls must reference the characters speaking the line by name. 
# Create test cases for these new calls. 
# Document the APIs similar to what I did in the endpoints for assignment 1.


@router.get("/lines/{line_id}", tags=["lines"])
def get_line(line_id: int):
    """
    This endpoint returns a single the corresponding line id that is queried by the user. For each line
    it returns:
    * `line_id` : the internal id of the line
    * `movie_title` : name of the movie
    * `character` : the character that spoke the line
    * `line_text` : the line spoken
    Some type of sorting mechanic will be implemented here (probably by : character, length of line text)
    """
    json = None
    
    for line in db.lines:
        if line["line_id"] == line_id:
            json = {
                "line_id": line["line_id"],
                "line_text": line["line_text"]
            }

    if json is None:
        raise HTTPException(status_code=404, detail = "line not found")
    return json

@router.get("/lines/", tags=["lines"])
def get_convo(line_id: int):
    """
    This endpoint returns a list of conversations. For each conversation it returns:
    * `movie_id`: the internal id of the movie that the conversation appears in
    * `movie_title`: The title of the movie.
    * `movie_year`: The year the movie was released.
    * `number_of_lines`: 
    * `imdb_votes`: The number of IMDB votes for the movie.
    """
    json = None
    return None

@router.get("/lines/{convo_id}", tags=["lines"])
def get_line_convo(line_id: int):
    """
    Documentation for function goes here.
    """
    json = None
    return None
