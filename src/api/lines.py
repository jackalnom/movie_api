from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from collections import Counter

router = APIRouter()

@router.get("/lines/{id}", tags=["lines"])
def get_line(id: str):
    """
    This endpoint returns a single line by its identifier. For each line
    it returns:
    * `line_id`: the internal id of the line. Can be used to query the 
       `/lines/{line_id}` endpoint. 
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `movie_id`: the internal id of the movie.
    * `conversation_id`: the internal id of the conversation
    * `line_text`: the text of the line 
    """

    # get line
    try:
        line = db.lines[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Line not found")

    result = {
        "line_id": int(id),
        "character_id": int(line["character_id"]),
        "movie_id": int(line["movie_id"]),
        "conversation_id": int(line["conversation_id"]),
        "line_text": line["line_text"] or None
    }
    return result


class line_sort_options(str, Enum):
    line_id = "line_id"
    line_length = "line_length"

@router.get("/lines/", tags=["lines"])
def list_character_lines(
    character_id: int = 0,
    limit: int = 50,
    offset: int = 0,
    sort: line_sort_options = line_sort_options.line_id,
):
    """
    This endpoint returns a list of lines that are spoken 
    by the given character_id query parameter. It returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character speaking the line.
    * `lines`: a list of objects where each contins 
    
    Each object in lines contains 
    * `line_id`: the internal id of the line.
    * `conversation_id`: the internal id of the conversation
    * `other_character_id`: the internal id of the other character in the conversation
    * `line_text`: the text of the line 

    You can filter for lines who are spoken by a character by the 
    `character_id` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `line_id` - Sort by line_id in ascending order.
    * `line_length` - Sort by line_length in ascending order.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    def get_sort_key(char):
        if sort == line_sort_options.line_id:
            return char['line_id']
        elif sort == line_sort_options.line_length:
            return char['line_length']
        
    # get character
    try:
        character = db.characters[str(character_id)]
    except KeyError:
        raise HTTPException(status_code=404, detail="Character not found")

    # get lines with the query character_id
    lines = []
    for line_id, line_data in db.lines.items():
        if character_id == int(line_data['character_id']):
            convo_id = int(line_data['conversation_id'])

            other_character_id = None
            for conversation_id, conversation_data in db.conversations.items():
                if int(conversation_id) == convo_id:
                    char1_id, char2_id = map(int, [conversation_data['character1_id'], conversation_data['character2_id']])
                    other_character_id = char2_id if character_id == char1_id else char1_id

            line_text = line_data['line_text']
            line_len = len(line_text) if line_text else 0
        
            line = {
                'line_id': int(line_id),
                'conversation_id': convo_id,
                'other_character_id': other_character_id,
                'line_text': line_text or None,
                'line_length': line_len
            }
            lines.append(line)
   
    # sort lines
    lines = sorted(lines, key=get_sort_key)
    
    # apply pagination
    lines = lines[offset : offset + limit]
    
    return {
        "character_id": character_id,
        "character": character["name"] or None,
        "lines": lines
    }

@router.get("/movie_lines/", tags=["lines"])
def list_movie_lines(
    movie_id: int = 0,
    limit: int = 50,
    offset: int = 0,
    sort: line_sort_options = line_sort_options.line_id,
):
    """
    This endpoint returns a list of lines that are in 
    the given movie_id query parameter. It returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movie/{movie_id}` endpoint.
    * `movie`: The name of the movie.
    * `lines`: a list of objects where each contins 
    
    Each object in lines contains 
    * `line_id`: the internal id of the line.
    * `conversation_id`: the internal id of the conversation
    * `other_character_id`: the internal id of the other character in the conversation
    * `line_text`: the text of the line 

    You can filter for lines who are spoken by a character by the 
    `character_id` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `line_id` - Sort by line_id in ascending order.
    * `line_length` - Sort by line_length in ascending order.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    def get_sort_key(char):
        if sort == line_sort_options.line_id:
            return char['line_id']
        elif sort == line_sort_options.line_length:
            return char['line_length']

    # get movie
    movie_info = db.movies.get(str(movie_id))
    if movie_info is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # get lines with the query movie_id
    lines = []
    for line_id, line_data in db.lines.items():
        if movie_id == int(line_data['movie_id']):
            convo_id = int(line_data['conversation_id'])
            character_id = int(line_data['character_id'])

            other_character_id = None
            for conversation_id, conversation_data in db.conversations.items():
                if int(conversation_id) == convo_id:
                    char1_id, char2_id = map(int, [conversation_data['character1_id'], conversation_data['character2_id']])
                    other_character_id = char2_id if character_id == char1_id else char1_id

            line_text = line_data['line_text']
            line_len = len(line_text) if line_text else 0
        
            line = {
                'line_id': int(line_id),
                'conversation_id': convo_id,
                'other_character_id': other_character_id,
                'line_text': line_text or None,
                'line_length': line_len
            }
            lines.append(line)
   
    # sort lines
    lines = sorted(lines, key=get_sort_key)
    
    # apply pagination
    lines = lines[offset : offset + limit]
    
    return {
        "movie_id": movie_id,
        "movie": movie_info["title"] or None,
        "lines": lines
    }
