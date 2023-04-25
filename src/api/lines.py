from fastapi import APIRouter, HTTPException
from src import database as db

router = APIRouter()

# Assignment 2
# test cases are in tests/test_lines.py

@router.get("/lines/{line_id}", tags=["lines"])
def get_line(line_id: int):
    """
    This endpoint returns a single the corresponding line id that is queried by the user. For each line
    it returns:
    * `line_id` : the internal id of the line
    * `movie_title` : name of the movie
    * `character` : the character that spoke the line
    * `line_text` : the line spoken
    """
    json = None

    if line_id in db.lines:
        tmp = db.lines[line_id]
        #print(tmp)
        json = {
            "line_id": line_id,
            "movie_title": db.movies[tmp.movie_id].title,
            "character": db.characters[tmp.c_id].name,
            "line_text" : tmp.line_text
        }

    if json is None:
        raise HTTPException(status_code=404, detail = "line not found")
    return json

@router.get("/character_lines/", tags=["lines"])
def get_character_and_movie(
    character_name: str,
    movie_title: str
    ):

    """
    This endpoint returns all lines a queried character has in a certain movie
    it returns:
    * `movie_id`: the internal id of the movie that the conversation appears in
    * `movie_title` : The title of the movie.
    * `movie_year` : The year the movie was released.
    * `character_id` : the id of the character
    * `character_name` : the name of the character
    * `lines`: an array of lines that the character had in the movie 
    """

    json = None
    lines = []

    for character in db.characters.items():
        if character[1].name.lower() == character_name.lower():
            print(character)
            if db.movies[character[1].movie_id].title.lower() == movie_title.lower():
                json = {
                    "movie_id" : character[1].movie_id,
                    "movie_title" : db.movies[character[1].movie_id].title,
                    "movie_year" : db.movies[character[1].movie_id].year,
                    "character_id" : character[0],
                    "character_name" : character[1].name
                }
    
                sorted_lines = [value for key, value in sorted(db.lines.items())]
                for line in sorted_lines:
                    if line.c_id == json["character_id"]:
                        lines.append(line.line_text)
                json["lines"] = lines
        
    if json is None:
        raise HTTPException(status_code=404, detail = "character or movie not found")

    return json

@router.get("/convo_lines/{convo_id}", tags=["lines"])
def get_line_convo(convo_id: int):

    # test w 30064

    """
    This endpoint returns the dialogue between two characters given the queried conversation id
    it returns:
    * `movie_title` : The title of the movie
    * `character1_name` : the name of character 1 in the dialogue
    * `character2_name` : the name of character 2 in the dialogue
    *  `conversation`: an array of the line text in order of what was said, with the character name
    of who is speaking to the left of the line.
    """

    json = None

    if convo_id in db.conversations:
        tmp = db.conversations[convo_id]
        json = {
            "movie_id": db.movies[tmp.movie_id].title,
            "character1_name": db.characters[tmp.c1_id].name,
            "character2_name": db.characters[tmp.c2_id].name
        }

        conversation = []
         
        sorted_lines = [value for key, value in sorted(db.lines.items())]
        for line in sorted_lines:
            if line.conv_id == convo_id:
                movie_line = db.characters[line.c_id].name + " : " + line.line_text
                conversation.append(movie_line)
        json["conversation"] = conversation

    if json is None:
        raise HTTPException(status_code=404, detail = "conversation not found")
    
    return json
