from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

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
    top_conversations = []
    processed_convo = {}
    for character in db.characters:
        if character["character_id"] == id:  
          filtered_convos = list(filter(lambda x: 
            (x["character1_id"] == id or x["character2_id"] == id), db.conversations))
          for convo in filtered_convos:
              filtered_lines = list(filter(lambda x: (x["conversation_id"] == convo["conversation_id"]), db.lines))
              processed_lines = max(filtered_lines, key = lambda x: x["line_sort"])
              char_id = ( convo["character2_id"] if convo["character1_id"] == id  else convo["character1_id"])
              processed_convo = {
                  "character_id" : int(char_id),
                  "character": db.characters[int(char_id)]["name"],
                  "gender" : db.characters[int(char_id)]["gender"] if db.characters[int(char_id)]["gender"] != "" else None ,
                  "number_of_lines_together" : int(processed_lines["line_sort"])
              }
              contains = False
              for entry in top_conversations:
                  if(int(entry["character_id"]) == int(char_id)):
                    contains = True
              if contains:
                  entry["number_of_lines_together"] = int(entry["number_of_lines_together"]) + int(processed_lines["line_sort"])
              else:
                  top_conversations.append(processed_convo)
                           
          json = { "character_id": int(id),
                   "character" : character["name"],
                   "movie" : db.movies[int(character["movie_id"])]["title"],
                   "gender" : character["gender"],
                   "top_conversations" : sorted(top_conversations, key = lambda x: x["number_of_lines_together"], reverse = True)
           }
    
    if json is None:
        raise HTTPException(status_code=404, detail="character not found.")

    return json


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
    character_list = []
    filtered_movie = {}
    filtered_lines = {}
    temp = sorted(db.characters, key = lambda x: x["character_id"]) 
    if (character_sort_options == character_sort_options.character):
        temp = sorted(temp, key = lambda x: x["name"])
    elif (character_sort_options == character_sort_options.movie):
        temp = sorted(temp, key = lambda x: x["movie_id"])
    else:
        temp = sorted(temp, key = lambda x: x["number_of_lines"])

    sorted_characters = sorted(temp, key= lambda x: x["name"] == "")
    for i in range(offset, limit):
        if i < len(sorted_characters):
          movie_id = int(sorted_characters[i]["movie_id"])
          for movie in db.movies:
            if (int(movie["movie_id"]) == movie_id):
              filtered_movie = movie
              break
          filtered_lines = list(filter(lambda x: (x["character_id"] == sorted_characters[i]["character_id"]), db.lines))

          character_json = { "character_id": int(sorted_characters[i]["character_id"]),
                   "character" : sorted_characters[i]["name"],
                   "movie" : filtered_movie["title"],
                   "number_of_lines" : len(filtered_lines)}
          character_list.append(character_json)
    
    return character_list
