from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
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

def sort_dict_by_num_lines(dictionary):
    sorted_dict = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1]['num_lines'], reverse=True)}
    return sorted_dict

def get_top_conv_characters(character):
    c_id = character.id
    movie_id = character.movie_id
    all_convs = filter(
        lambda conv: conv.movie_id == movie_id
        and (conv.c1_id == c_id or conv.c2_id == c_id),
        db.conversations.values(),
    )
    line_counts = Counter()

    for conv in all_convs:
        other_id = conv.c2_id if conv.c1_id == c_id else conv.c1_id
        line_counts[other_id] += conv.num_lines

    return line_counts.most_common()


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
<<<<<<< HEAD
    # get character
    try:
        character = db.characters[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Character not found")

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

=======

    character = db.characters.get(id)

    if character:
        movie = db.movies.get(character.movie_id)
        result = {
            "character_id": character.id,
            "character": character.name,
            "movie": movie and movie.title,
            "gender": character.gender,
            "top_conversations": (
                {
                    "character_id": other_id,
                    "character": db.characters[other_id].name,
                    "gender": db.characters[other_id].gender,
                    "number_of_lines_together": lines,
                }
                for other_id, lines in get_top_conv_characters(character)
            ),
        }
        return result

    raise HTTPException(status_code=404, detail="character not found.")
>>>>>>> db993774e9cc922cd0a443a79a1314fde568e413


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

<<<<<<< HEAD
    def get_sort_key(char):
        if sort == character_sort_options.character:
            return char['character']
        elif sort == character_sort_options.movie:
            return char['movie']
        elif sort == character_sort_options.number_of_lines:
            return -char['number_of_lines']

    # retrieve characters from database
    characters = []
    for char_id, char_data in db.characters.items():
        if name.lower() in char_data['name'].lower():
            char = {
                'character_id': int(char_id),
                'character': char_data['name'],
                'movie': db.movies[char_data['movie_id']]['title'],
                'number_of_lines': len([line for line in db.lines.values() if line['character_id'] == char_id])
            }
            characters.append(char)
    
    # sort characters
    characters = sorted(characters, key=get_sort_key)
    
    # apply pagination
    characters = characters[offset : offset + limit]
    
    return characters
=======
    if name:

        def filter_fn(c):
            return c.name and name.upper() in c.name

    else:

        def filter_fn(_):
            return True

    items = list(filter(filter_fn, db.characters.values()))

    def none_last(x, reverse=False):
        return (x is None) ^ reverse, x

    if sort == character_sort_options.character:
        items.sort(key=lambda c: none_last(c.name))
    elif sort == character_sort_options.movie:
        items.sort(key=lambda c: none_last(db.movies[c.movie_id].title))
    elif sort == character_sort_options.number_of_lines:
        items.sort(key=lambda c: none_last(c.num_lines, True), reverse=True)

    json = (
        {
            "character_id": c.id,
            "character": c.name,
            "movie": db.movies[c.movie_id].title,
            "number_of_lines": c.num_lines,
        }
        for c in items[offset : offset + limit]
    )
    return json
>>>>>>> db993774e9cc922cd0a443a79a1314fde568e413
