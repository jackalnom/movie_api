import sqlalchemy
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


@router.get("/lines/{line_id}", tags=["lines"])
def get_line_by_id(line_id: str):
    """
    This endpoint returns a single line by its identifier. For each line it returns:
    * `line_id`: the internal id of the line.
    * `movie`: The name of the movie in which this line was spoken
    * `character1`: The name of the character who spoke the line
    * `character2`: The name of the character this line was spoken to
    * `line_content`: The content of the line
    """
    characters2 = sqlalchemy.alias(db.characters)

    stmt = (
        sqlalchemy.select(
            db.lines.c.line_id,
            db.movies.c.title,
            db.characters.c.name.label("character1"),
            characters2.c.name.label("character2"),
            db.lines.c.line_text
        )
            .select_from(
            db.lines.join(db.conversations, db.conversations.c.conversation_id == db.lines.c.conversation_id)
                .join(db.characters, db.conversations.c.character1_id == db.characters.c.character_id)
                .join(characters2, db.conversations.c.character2_id == characters2.c.character_id)
                .join(db.movies, db.movies.c.movie_id == db.lines.c.movie_id)
        )
            .where(db.lines.c.line_id == line_id)
            .group_by(
            db.lines.c.line_id,
            db.movies.c.title,
            db.characters.c.name,
            characters2.c.name,
            db.lines.c.line_text
        )
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="line not found.")
        for row in result:
            json = {
                "line_id": row.line_id,
                "movie": row.title,
                "character1": row.character1,
                "character2": row.character2,
                "line_content": row.line_text,
            }
    return json


@router.get("/lines/movie/{movie_id}", tags=["lines"])
def list_lines_by_movie(movie_id: str):
    """
    This endpoint returns a list of lines that are in the movie of the given movie_id. For each line it returns:
    * `line_id`: the internal id of the line.
    * `movie`: The name of the movie in which this line was spoken
    * `character1`: The name of the character who spoke the line
    * `character2`: The name of the character this line was spoken to
    * `line_content`: The content of the line
    """
    characters1 = sqlalchemy.alias(db.characters)
    characters2 = sqlalchemy.alias(db.characters)

    stmt = (
        sqlalchemy.select(
            db.lines.c.line_id,
            db.movies.c.title,
            characters1.c.name.label("character1"),
            characters2.c.name.label("character2"),
            db.lines.c.line_text,
        )
            .select_from(
            db.lines.join(db.conversations, db.conversations.c.conversation_id == db.lines.c.conversation_id)
                .join(characters1, characters1.c.character_id == db.conversations.c.character1_id)
                .join(characters2, characters2.c.character_id == db.conversations.c.character2_id)
                .join(db.movies, db.movies.c.movie_id == db.lines.c.movie_id)
        )
            .where(db.lines.c.movie_id == movie_id)
            .group_by(
            db.lines.c.line_id,
            db.movies.c.title,
            characters1.c.name,
            characters2.c.name,
            db.lines.c.line_text,
        )
            .order_by(db.lines.c.line_id)
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        jsons = []
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="line not found.")
        for row in result:
            json = {
                "line_id": row.line_id,
                "movie": row.title,
                "character1": row.character2,
                "character2": row.character1,
                "line_content": row.line_text,
            }
            jsons.append(json)
    return jsons


@router.get("/lines/character/", tags=["lines"])
def list_lines_by_character(
    character: str = "",
    limit: int = 50,
    offset: int = 0,
):
    """
    This endpoint returns a list of lines. For each line it returns:
    * `line_id`: the internal id of the line.
    * `movie`: The name of the movie in which this line was spoken
    * `character1`: The name of the character who spoke the line
    * `character2`: The name of the character this line was spoken to
    * `line_content`: The content of the line

    You can filter for lines whose speaking character contain a string by using the
    `character` query parameter.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    characters2 = sqlalchemy.alias(db.characters)

    stmt = (
        sqlalchemy.select(
            db.lines.c.line_id,
            db.movies.c.title,
            db.characters.c.name.label("character1"),
            characters2.c.name.label("character2"),
            db.lines.c.line_text
        )
            .select_from(
            db.lines.join(db.conversations, db.conversations.c.conversation_id == db.lines.c.conversation_id)
                .join(db.characters, db.conversations.c.character1_id == db.characters.c.character_id)
                .join(characters2, db.conversations.c.character2_id == characters2.c.character_id)
                .join(db.movies, db.movies.c.movie_id == db.lines.c.movie_id)
        )
            .limit(limit)
            .offset(offset)
            .group_by(
            db.lines.c.line_id,
            db.movies.c.title,
            db.characters.c.name,
            characters2.c.name,
            db.lines.c.line_text
        )
    )

    if character != "":
        character = character.upper()
        stmt = stmt.where(db.characters.c.name.like(f"%{character}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        print(result)
        jsons = []
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="line not found.")
        for row in result:
            json = {
                "line_id": row.line_id,
                "movie": row.title,
                "character1": row.character1,
                "character2": row.character2,
                "line_content": row.line_text,
            }
            jsons.append(json)
    return jsons
    # json = []
    # temp = []
    # # json every movie
    # for line in db.lines:
    #     json_temp = {'line_id': line.line_id,
    #                  'movie': db.moviesWithLines[line.movie_id][0].title,
    #                  'character1': db.charsWithConvos[line.character_id][0].name,
    #                  'character2': db.charsWithConvos[db.convoDictByID[line.conversation_id].character2_id][0].name,
    #                  'line_content': line.line_text}
    #     json.append(json_temp)
    # # sort by movie name
    # json = sorted(json, key=lambda d: d['movie'])
    # # filter lines by character name
    # if len(character) > 0:
    #     for j in json:
    #         if character.upper() in j['character1'].upper():
    #             temp.append(j)
    #     json = temp
    # # return correct number of items
    # if len(json) <= offset:
    #     return {}
    # elif len(json) <= offset + limit:
    #     return json[offset:]
    # else:
    #     return json[offset:offset + limit]
