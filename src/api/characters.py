from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import json

from fastapi.params import Query
from src import database as db
from collections import Counter

from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy

router = APIRouter()

@router.get("/characters/{id}", tags=["characters"])
def get_character(id: int):
    """
    This endpoint returns a single character by its identifier. For each character
    it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `gender`: The gender of the character.
    * `top_conversations`: A list of characters that the character has the most
      conversations with. The characters are listed in order of the number of
      lines together. These conversations are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * `number_of_lines_together`: The number of lines the character has with the
      originally queried character.
    """
    # Create a single connection to the database. Later we will discuss pooling connections.
    conn = db.engine.connect()

    stmnt = (sqlalchemy.text("""
    SELECT character_id, name, movies.title, gender
    FROM characters
    JOIN movies ON characters.movie_id = movies.movie_id
    WHERE character_id = :char_id
    """))
    
    # Execute the query with the provided character ID and fetch the results
    result = conn.execute(stmnt, {"char_id" : str(id)}).fetchall()

    if len(result) == 0:
      raise HTTPException(status_code=404, detail="character not found.")

    character = {
        "character_id": result[0][0],
        "character": result[0][1],
        "movie": result[0][2],
        "gender": result[0][3],
    }

    return character
    
class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"

@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: character_sort_options = character_sort_options.character,
):
    
    """
    This endpoint returns a list of characters. For each character it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `number_of_lines`: The number of lines the character has in the movie.

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `number_of_lines` - Sort by number of lines, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    stmnt0 = (sqlalchemy.text("""
    SELECT characters.character_id, characters.name, movies.title, COUNT(lines.line_id) AS number_of_lines
    FROM characters
    JOIN movies ON characters.movie_id = movies.movie_id
    JOIN lines ON characters.character_id = lines.character_id
    WHERE characters.name LIKE :name
    GROUP BY characters.character_id, movies.title
    Order BY characters.name
    LIMIT :limit
    OFFSET :offset
    """))

    stmnt1 = (sqlalchemy.text("""
    SELECT characters.character_id, characters.name, movies.title, COUNT(lines.line_id) AS number_of_lines
    FROM characters
    JOIN movies ON characters.movie_id = movies.movie_id
    JOIN lines ON characters.character_id = lines.character_id
    WHERE characters.name LIKE :name
    GROUP BY characters.character_id, movies.title
    Order BY movies.title
    LIMIT :limit
    OFFSET :offset
    """))

    stmnt2 = (sqlalchemy.text("""
    SELECT characters.character_id, characters.name, movies.title, COUNT(lines.line_id) AS number_of_lines
    FROM characters
    JOIN movies ON characters.movie_id = movies.movie_id
    JOIN lines ON characters.character_id = lines.character_id
    WHERE characters.name LIKE :name
    GROUP BY characters.character_id, movies.title
    Order BY number_of_lines desc
    LIMIT :limit
    OFFSET :offset
    """))

    conn = db.engine.connect()

    params = {
        "name": f"%{name.upper()}%",
        "limit": limit,
        "offset": offset
    }

    curr_statement = ""

    if sort.value == "character":
       curr_statement = stmnt0
    elif sort.value == "movie":
       curr_statement = stmnt1
    else:
       curr_statement = stmnt2
       
    result = conn.execute(curr_statement, params).fetchall()

    if len(result) == 0:
      raise HTTPException(status_code=404, detail="no characters found")

    returnval = []
    for row in result:
       character = {
          "character_id": row[0],
          "character": row[1],
          "movie": row[2],
          "number_of_lines": row[3]
       }
       returnval.append(character)

    return returnval

