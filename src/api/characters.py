from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
import json

router = APIRouter()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: str):
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
    json_return = None
    for character in db.characters:
        if character.character_id == int(id):
            print("character found")
            charConvos = []
            for char in db.charsWithConvos[int(id)][1]:
                currentChar = db.charsWithConvos[char][0]
                temp_json = {'character_id': char,
                             'character': currentChar.name,
                             'gender': currentChar.gender,
                             'number_of_lines_together': db.charsWithConvos[int(id)][1][char]}
                charConvos.append(temp_json)
            charConvos = sorted(charConvos, key=lambda d: d['number_of_lines_together'], reverse=True)
            json_return = {'character_id': character.character_id,
                           'character': character.name.upper(),
                           'movie': db.moviesWithLines[character.movie_id][0].title,
                           'gender': character.gender,
                           'top_conversations': charConvos}

    if json_return is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return json_return


class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
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
    json = []
    # temp will hold characters that pass filter
    temp = []
    # json every character
    for character in db.characters:
        json_temp = {'character_id': character.character_id,
                     'character': character.name.upper(),
                     'movie': db.moviesWithLines[character.movie_id][0].title,
                     'number_of_lines': db.charsWithConvos[character.character_id][2]}
        json.append(json_temp)
    # filter characters by name
    if len(name) > 0:
        for j in json:
            if name.upper() in j['character']:
                temp.append(j)
        json = temp
    # sort remaining characters
    if sort == character_sort_options.character:
        json = sorted(json, key=lambda d: d['character'])
    elif sort == character_sort_options.movie:
        json = sorted(json, key=lambda d: d['movie'])
    elif sort == character_sort_options.number_of_lines:
        json = sorted(json, key=lambda d: d['number_of_lines'], reverse=True)
    # return correct number of items
    if len(json) <= offset:
        return {}
    elif len(json) <= offset+limit:
        return json[offset:]
    else:
        return json[offset:offset+limit]
