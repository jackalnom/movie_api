from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from collections import Counter
import sqlalchemy

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
    * `character_name`: the name of the character who gives the line. 
    * `movie_id`: the internal id of the movie.
    * `conversation_id`: the internal id of the conversation
    * `line_text`: the text of the line 
    """

    with db.engine.connect() as conn:
        res = conn.execute(
            sqlalchemy.text("""
            SELECT 
                lines.line_id, 
                lines.character_id, 
                characters.name AS character_name, 
                lines.movie_id, 
                lines.conversation_id, 
                lines.line_text
            FROM 
                lines 
                JOIN characters ON lines.character_id = characters.character_id
            WHERE 
                lines.line_id = :x
            """), [{"x": int(id)}]
        ).fetchone()    

        if res is None:
            raise HTTPException(status_code=404, detail="line not found.")

    return {
        "line_id": res.line_id,
        "character_id": res.character_id,
        "character_name": res.character_name,
        "movie_id": res.movie_id,
        "conversation_id": res.conversation_id,
        "line_text": res.line_text
    }


@router.get("/lines/", tags=["lines"])
def list_character_lines(
    character_id: int = 0,
    limit: int = 50,
    offset: int = 0,
):
    """
    This endpoint returns a list of lines that are spoken 
    by the given character_id query parameter. It returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character speaking the line.
    * `lines`: a list of objects where each contins 
    
    Each object in lines contains 
    * `line_id`: the internal id of the line.
    * `conversation_id`: the internal id of the conversation
    * `line_text`: the text of the line 

    You can filter for lines who are spoken by a character by the 
    `character_id` query parameter.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    with db.engine.connect() as conn:
        result_a = conn.execute(
            sqlalchemy.text("""
            SELECT
                characters.character_id,
                characters.name AS character
            FROM characters
            WHERE characters.character_id = :x
            """), [{"x": character_id}]
        ).fetchone()

        if result_a is None:
            raise HTTPException(status_code=404, detail="character not found.")
    
        result_b = conn.execute(
            sqlalchemy.text("""
            SELECT
                characters.character_id,
                lines.line_id,
                lines.line_text,
                conversations.conversation_id
            FROM 
                characters 
                JOIN lines ON lines.character_id = characters.character_id
                JOIN conversations ON lines.conversation_id = conversations.conversation_id
            WHERE 
                characters.character_id = :x
            ORDER BY 
                lines.line_id DESC 
            LIMIT :limit
            OFFSET :offset
            """), [{"x": character_id,
                    "limit": limit,
                    "offset": offset}]
        ).fetchall()

        lines = []
        for row in result_b:
            lines.append({
                "line_id": row.line_id,
                "conversation_id": row.conversation_id,
                "line_text": row.line_text
            })
    
    return {
        "character_id": result_a.character_id,
        "character": result_a.character or None,
        "lines": lines
    }

@router.get("/movie-lines/", tags=["lines"])
def list_movie_lines(
    movie_id: int = 0,
    limit: int = 50,
    offset: int = 0,
):
    """
    This endpoint returns a list of lines that are in 
    the given movie_id query parameter. It returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movie/{movie_id}` endpoint.
    * `movie`: The name of the movie.
    * `lines`: a list of objects where each contins 
    
    Each object in lines contains 
    * `line_id`: the internal id of the line.
    * `conversation_id`: the internal id of the conversation
    * `character_id`: the internal id of the character who gives the line.
    * `character_name`: the name of the character who gives the line.
    * `line_text`: the text of the line 

    You can filter for lines who are spoken by a character by the 
    `character_id` query parameter.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    with db.engine.connect() as conn:
        result_a = conn.execute(
            sqlalchemy.text("""
            SELECT
                movies.movie_id,
                movies.title AS movie
            FROM movies
            WHERE movies.movie_id = :x
            """), [{"x": movie_id}]
        ).fetchone()

        if result_a is None:
            raise HTTPException(status_code=404, detail="movie not found.")
    
        result_b = conn.execute(
            sqlalchemy.text("""
            SELECT
                lines.line_id,
                conversations.conversation_id,
                characters.character_id,
                characters.name,
                lines.line_text
            FROM 
                movies 
                JOIN lines ON lines.movie_id = movies.movie_id
                JOIN conversations ON lines.movie_id = conversations.movie_id
                JOIN characters ON lines.movie_id = characters.movie_id
            WHERE 
                movies.movie_id = :x
            ORDER BY 
                lines.line_id DESC 
            LIMIT :limit
            OFFSET :offset
            """), [{"x": movie_id,
                    "limit": limit,
                    "offset": offset}]
        ).fetchall()

        lines = []
        for row in result_b:
            lines.append({
                "line_id"    : row.line_id,
                "conversation_id": row.conversation_id,
                "character_id": row.character_id,
                "character_name": row.name,
                "line_text"    : row.line_text
            })
    
    return {
        "movie_id": movie_id,
        "movie": result_a.movie or None,
        "lines": lines
    }
