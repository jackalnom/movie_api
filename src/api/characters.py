from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from collections import Counter

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

    # new json needs: charID, character, movie, gender
    json = None
    for character in db.characters:
        if character["character_id"] == id:
            json = {
              "character_id": id,
              "character": character["name"],
              "movie": get_movie(character["movie_id"]),
              "gender" : character["gender"]
            }

            id = json["character_id"]

            lines_dict = {}
            for convo in db.conversations:
              if id == convo["character1_id"]:
                if convo["character2_id"] in lines_dict:
                  lines_dict[convo["character2_id"]] += count_lines(convo["conversation_id"])
                else:
                  lines_dict[convo["character2_id"]] = count_lines(convo["conversation_id"])
              if id == convo["character2_id"]:
                if convo["character1_id"] in lines_dict:
                  lines_dict[convo["character1_id"]] += count_lines(convo["conversation_id"])
                else:
                  lines_dict[convo["character1_id"]] = count_lines(convo["conversation_id"])
            
            sorted_list = sorted(lines_dict.items(), key = lambda x:x[1], reverse = True)

            convo_list = []
            for item in sorted_list:
              tmp = get_character(item[0])
              new_object = {
                "character_id": item[0],
                "character": tmp["name"],
                "gender": tmp["gender"],
                "number_of_lines_together": item[1]
              }
              convo_list.append(new_object)
            json["top_conversations"] = convo_list            

    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")
    return json

# some helpers

def get_movie(movie_id: int):
  for movie in db.movies:
     if movie["movie_id"] == movie_id:
        return movie["title"]

def get_character(character_id: int):
  for character in db.characters:
    if character["character_id"] == character_id:
      return character

def get_character_lines(character_id: int):
  counter = 0
  for line in db.lines:
    if line["character_id"] == character_id:
      counter += 1
  return counter

# helper function to help find count of how many lines there given a convo_id (int)
def count_lines(convo_id: int):
  counter = 0
  for line in db.lines:
    if line["conversation_id"] == convo_id:
      counter += 1
  return counter

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

    # current a WIP
    json_list = []
    # check for limit
    i = 0
    while (i < len(db.characters)):
      pass
      
    json = None
    return json
