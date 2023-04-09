from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from collections import Counter

router = APIRouter()

def get_convo_stats(id):
    convo_stats = {}
    for convo_id, convo in db.conversations.items():
        if (convo['character1_id'] != id) and (convo['character2_id'] != id):
            continue
        
        char1_id, char2_id = convo['character1_id'], convo['character2_id']
        other_char_id = char2_id if id == char1_id else char1_id

        if other_char_id not in convo_stats:
            convo_stats[other_char_id] = {'num_lines': 0, 'convo_ids': []}

        for line_id, line in db.lines.items():
            if convo_id == line["conversation_id"]:
                convo_stats[other_char_id]['num_lines'] += 1
        convo_stats[other_char_id]['convo_ids'].append(int(convo_id))
    return convo_stats

def convo_stats_to_top_convos(convo_stats):
    top_convos = []
    for convo_stat_id, convo_stat in convo_stats.items():
        char = db.characters[str(convo_stat_id)]
        item = {
            "character_id": int(convo_stat_id),
            "character": char["name"],
            "gender": char["gender"],
            "number_of_lines_together": int(convo_stat["num_lines"])
        }
        top_convos.append(item)
    return top_convos



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
    # get character and movie 
    json = None
    character = db.characters[id]

    movie_title = ""
    for movie_id, movie in db.movies.items():
        if character["movie_id"] == movie_id:
            movie_title = movie["title"]

    convo_stats = get_convo_stats(id)

    # sort based on num_lines, from greatest to least 
    convo_stats = sort_dict_by_num_lines(convo_stats)

    # transform convo_stats into top_conversations desired json form
    top_convos = convo_stats_to_top_convos(convo_stats)
    
    out = {
        "character_id": int(id),
        "character": character["name"],
        "movie": movie_title,
        "gender": character["gender"] or None,
        "top_conversations": top_convos
    }
    print("GET CHARACTER: ", out)
    return out 

def sort_dict_by_num_lines(dictionary):
    sorted_dict = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1]['num_lines'], reverse=True)}
    return sorted_dict


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

    json = None
    return json
