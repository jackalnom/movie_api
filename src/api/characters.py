from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
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

    with db.engine.connect() as conn:
        result_a = conn.execute(
            sqlalchemy.text("""
            SELECT
                characters.character_id,
                characters.name AS character,
                movies.title AS movie,
                characters.gender
            FROM characters
            JOIN movies ON characters.movie_id = movies.movie_id
            WHERE characters.character_id = :x
            """), [{"x": id}]
        ).fetchone()

        if result_a is None:
            raise HTTPException(status_code=404, detail="character not found.")


        result_b = conn.execute(
            sqlalchemy.text("""
            SELECT 
                (CASE
                    WHEN characters.character_id IN (conversations.character1_id) THEN conversations.character2_id
                    WHEN characters.character_id IN (conversations.character2_id) THEN conversations.character1_id
                END) AS other_char_id,
            SUM(CASE 
                WHEN conversations.character1_id = characters.character_id THEN conversations.num_lines 
                WHEN conversations.character2_id = characters.character_id THEN conversations.num_lines 
                ELSE 0 
            END) AS number_of_lines_together,
            (CASE
                WHEN characters.character_id IN (conversations.character1_id) THEN 
                (SELECT characters.name FROM characters WHERE characters.character_id = conversations.character2_id)
                WHEN characters.character_id IN (conversations.character2_id) THEN 
                (SELECT characters.name FROM characters WHERE characters.character_id = conversations.character1_id)
            END) AS character,
            (CASE
                WHEN characters.character_id IN (conversations.character1_id) THEN 
                (SELECT characters.gender FROM characters WHERE characters.character_id = conversations.character2_id)
                WHEN characters.character_id IN (conversations.character2_id) THEN 
                (SELECT characters.gender FROM characters WHERE characters.character_id = conversations.character1_id)
            END) AS gender
            FROM 
                characters 
                JOIN conversations ON characters.character_id IN (conversations.character1_id, conversations.character2_id) 
                JOIN movies ON conversations.movie_id = movies.movie_id 
            WHERE 
                characters.character_id = :x
            GROUP BY 
                characters.character_id,
                conversations.character1_id,
                conversations.character2_id
            ORDER BY 
                number_of_lines_together DESC 
            """), 
            [{"x": id}]
        )
        top_convs = []
        for row in result_b.fetchall():
            top_convs.append({
                "character_id": row.other_char_id,
                "character": row.character,
                "gender": row.gender,
                "number_of_lines_together": row.number_of_lines_together
            })

        json = {
            "character_id": result_a.character_id,
            "character": result_a.character,
            "movie": result_a.movie,
            "gender": result_a.gender,
            "top_conversations": top_convs
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

    with db.engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text("""
            SELECT 
                characters.character_id, 
                characters.name AS character, 
                movies.title AS movie, 
                COUNT(lines.line_id) AS number_of_lines 
            FROM 
                characters
                JOIN movies ON characters.movie_id = movies.movie_id 
                JOIN lines ON characters.character_id = lines.character_id 
            WHERE
                characters.name LIKE :x
            GROUP by
                characters.character_id, 
                characters.name, 
                movies.title 
            ORDER by  
                CASE
                    WHEN :sort = 'character' THEN characters.name
                END ASC,
                CASE
                    WHEN :sort = 'movie' THEN movies.title
                END ASC,
                CASE
                    WHEN :sort NOT IN ('character', 'movie') THEN COUNT(lines.line_id)
                END DESC
            LIMIT :y
            OFFSET :z
            """),
            [{"x": "%" + name.upper() + "%",
              "y": limit,
              "z": offset,
              "sort": sort}]
        )
        json = []
        for row in result.fetchall():
            print(row)
            json.append(
                {
                    "character_id": row.character_id,
                    "character": row.character,
                    "movie": row.movie,
                    "number_of_lines": row.number_of_lines,
                }
            )
        return json

    """
    stmt = sqlalchemy.select(
            db.characters.c.character_id,
            db.characters.c.name.label('character'),
            db.movies.c.title.label('movie'),
            sqlalchemy.func.count(db.lines.c.line_id).label('number_of_lines')
        ).join(db.movies, db.characters.c.movie_id == db.movies.c.movie_id) \
        .join(db.lines, db.characters.c.character_id == db.lines.c.character_id) \
        .where(db.characters.c.name.like(f"%{name.upper()}%")) \
        .group_by(
            db.characters.c.character_id,
            db.characters.c.name,
            db.movies.c.title
        ).order_by(
            sqlalchemy.case(
                (sort == 'character', sqlalchemy.cast(db.characters.c.name, sqlalchemy.Text)),
                (sort == 'movie', sqlalchemy.cast(db.movies.c.title, sqlalchemy.Text)),
                else_=sqlalchemy.cast(sqlalchemy.func.count(db.lines.c.line_id), sqlalchemy.Text)
            ).desc()) \
        .limit(limit) \
        .offset(offset)
    
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result.fetchall():
            json.append(
                {
                    "character_id": row.character_id,
                    "character": row.character,
                    "movie": row.movie,
                    "number_of_lines": row.number_of_lines,
                }
            )

    return json
    """
