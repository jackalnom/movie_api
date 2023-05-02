import sqlalchemy
from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
from fastapi.params import Query
from sqlalchemy import case
from src import database as db

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
    # Get the character they asked for with its id, name, movie, and gender
    stmt = (
        sqlalchemy.select(
            db.characters.c.character_id,
            db.characters.c.name,
            db.movies.c.title,
            db.characters.c.gender,
        )
            .join(db.movies, db.movies.c.movie_id == db.characters.c.movie_id)
            .group_by(db.characters.c.character_id, db.characters.c.name, db.movies.c.title, db.characters.c.gender)
            .where(db.characters.c.character_id == id)
    )

    stmt2 = (
        sqlalchemy.select(
            db.characters.c.character_id,
            db.characters.c.name,
            db.characters.c.gender,
            sqlalchemy.func.count(db.lines.c.line_id).label("line_count")
        )
            .select_from(
            db.conversations.join(
                db.lines,
                db.conversations.c.conversation_id == db.lines.c.conversation_id
            ).join(
                db.characters,
                ((db.conversations.c.character1_id == db.characters.c.character_id) & (
                            db.conversations.c.character2_id == id)) |
                ((db.conversations.c.character2_id == db.characters.c.character_id) & (
                            db.conversations.c.character1_id == id))
            )
        )
            .group_by(db.characters.c.character_id, db.characters.c.name)
            .order_by(sqlalchemy.desc("line_count"))
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        result2 = conn.execute(stmt2)
        charJSON = []
        json = []
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="character not found.")
        for row in result2:
            charJSON.append(
                {
                    "character_id": row.character_id,
                    "character": row.name,
                    "gender": row.gender,
                    "number_of_lines_together": row.line_count,
                }
            )
        for row in result:
            json = {
                "character_id": row.character_id,
                "character": row.name,
                "movie": row.title,
                "gender": row.gender,
                "top_conversations": charJSON,
            }
    return json


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
    # First configure sort
    if sort is character_sort_options.character:
        order_by = db.characters.c.name
    elif sort is character_sort_options.movie:
        order_by = db.movies.c.title
    elif sort is character_sort_options.number_of_lines:
        order_by = sqlalchemy.desc("line_count")
    else:
        assert False

    # Get all necessary fields with the proper limit, offset, and sort
    stmt = (
        sqlalchemy.select(
            db.characters.c.character_id,
            db.characters.c.name,
            db.movies.c.title,
            sqlalchemy.func.count(db.lines.c.line_id).label("line_count"),
        )
            .join(db.lines, db.lines.c.character_id == db.characters.c.character_id)
            .join(db.movies, db.movies.c.movie_id == db.characters.c.movie_id)
            .limit(limit)
            .offset(offset)
            .group_by(db.characters.c.character_id, db.movies.c.title)
            .order_by(order_by, db.characters.c.character_id)
    )

    # filter only if name parameter is passed
    if name != "":
        stmt = stmt.where(db.characters.c.name.ilike(f"%{name}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append(
                {
                    "character_id": row.character_id,
                    "character": row.name,
                    "movie": row.title,
                    "number_of_lines": row.line_count,
                }
            )

    return json
