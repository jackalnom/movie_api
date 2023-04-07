from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from collections import Counter

router = APIRouter()



def most_common_number(arr):
    count = Counter(arr)
    most_common, num_occurrences = count.most_common(1)[0]
    return most_common, num_occurrences



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
    json = None
    character = db.characters[id]
    print(character)

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


    # convo_stats = {}
    # for line_id, line in db.lines.items():
    #     if line['character_id'] != id:
    #         continue
        
    #     convo_id = line['conversation_id']
    #     convo = db.conversations[convo_id]
    #     char1_id, char2_id = convo['character1_id'], convo['character2_id']
    #     other_char_id = char2_id if id == char1_id else char1_id
    
    #     if other_char_id not in convo_stats:
    #         convo_stats[other_char_id] = {'num_lines': 0, 'convo_ids': []}

    #     convo_stats[other_char_id]['num_lines'] += 1
    #     convo_stats[other_char_id]['convo_ids'].append(int(convo_id))
    print()
    print(convo_stats)
    print()

    max_num_lines_ele = None
    max_num_lines = -1
    for element in convo_stats.values():
        if element['num_lines'] > max_num_lines:
            max_num_lines_ele = element
            max_num_lines = element['num_lines']

    print(max_num_lines_ele)

    # most_common_convo_char, num_convos = most_common_number(convo_chars)
    # print(most_common_convo_char, num_convos)
    # print(json)
    return 

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
