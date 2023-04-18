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
    json = None
    for line in db.lines:
        if line.line_id == int(line_id):
            print("line found")
            json = {'line_id': line.line_id,
                    'movie': db.moviesWithLines[line.movie_id][0].title,
                    'character1': db.charsWithConvos[line.character_id][0].name,
                    'character2': db.charsWithConvos[db.convoDictByID[line.conversation_id].character2_id][0].name,
                    'line_content': line.line_text}

    if json is None:
        raise HTTPException(status_code=404, detail="line not found.")

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
    json = []
    # json every movie
    for line in db.lines:
        if line.movie_id == int(movie_id):
            json_temp = {'line_id': line.line_id,
                         'movie': db.moviesWithLines[line.movie_id][0].title,
                         'character1': db.charsWithConvos[line.character_id][0].name,
                         'character2': db.charsWithConvos[db.convoDictByID[line.conversation_id].character2_id][0].name,
                         'line_content': line.line_text}
            json.append(json_temp)
    # sort by movie name
    json = sorted(json, key=lambda d: d['movie'])
    if len(json) > 0:
        return json
    else:
        return {}


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
    json = []
    temp = []
    # json every movie
    for line in db.lines:
        json_temp = {'line_id': line.line_id,
                     'movie': db.moviesWithLines[line.movie_id][0].title,
                     'character1': db.charsWithConvos[line.character_id][0].name,
                     'character2': db.charsWithConvos[db.convoDictByID[line.conversation_id].character2_id][0].name,
                     'line_content': line.line_text}
        json.append(json_temp)
    # sort by movie name
    json = sorted(json, key=lambda d: d['movie'])
    # filter lines by character name
    if len(character) > 0:
        for j in json:
            if character.upper() in j['character1'].upper():
                temp.append(j)
        json = temp
    # return correct number of items
    if len(json) <= offset:
        return {}
    elif len(json) <= offset + limit:
        return json[offset:]
    else:
        return json[offset:offset + limit]
