from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


# include top 3 actors by number of lines
@router.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: str):
    """
    This endpoint returns a single movie by its identifier. For each movie it returns:
    * `movie_id`: the internal id of the movie.
    * `title`: The title of the movie.
    * `top_characters`: A list of characters that are in the movie. The characters
      are ordered by the number of lines they have in the movie. The top five
      characters are listed.

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `num_lines`: The number of lines the character has in the movie.

    """
    movie_info = db.movies.get(movie_id)
    if movie_info is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get the characters in the movie from the database
    characters = {}
    for line in db.lines.values():
        if line["movie_id"] == movie_id:
            character_id = line["character_id"]
            characters[character_id] = characters.get(character_id, {"num_lines": 0})
            characters[character_id]["num_lines"] += 1
            characters[character_id]["character_id"] = int(character_id)
            characters[character_id]["character"] = db.characters[character_id]["name"]
    characters = [characters[c] for c in sorted(characters, key=lambda c: characters[c]["num_lines"], reverse=True)][:5]
    # for character in characters:
    #     character.update(db.characters[character["character_id"]])
    
    # Assemble the movie information with the top characters
    result = {
        "movie_id": int(movie_id),
        "title": movie_info["title"],
        "top_characters": characters
    }
    return result

def get_char_stats(id):
    # find characters with given movie_id
    stats = []
    for char_id, char_data in db.characters.items():
        if id not in char_data['movie_id'].lower():
            continue 

        # find num lines in the movie 
        nlines = 0
        for line_id, line_data in db.lines.items():
            if (int(line_data['character_id']) == int(char_id)) and (id in line_data['movie_id'].lower()):
                nlines += 1

        stats.append({
            'character_id': int(char_id),
            'character': str(char_data['name']) or None,
            'num_lines': nlines
        })
    # sort based on num_lines, from greatest to least 
    stats = sorted(stats, key=lambda x: x['num_lines'], reverse=True)
    return stats[:5]

class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"

# Add get parameters
@router.get("/movies/", tags=["movies"])
def list_movies(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: movie_sort_options = movie_sort_options.movie_title,
):
    """
    This endpoint returns a list of movies. For each movie it returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movies/{movie_id}` endpoint.
    * `movie_title`: The title of the movie.
    * `year`: The year the movie was released.
    * `imdb_rating`: The IMDB rating of the movie.
    * `imdb_votes`: The number of IMDB votes for the movie.

    You can filter for movies whose titles contain a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `movie_title` - Sort by movie title alphabetically.
    * `year` - Sort by year of release, earliest to latest.
    * `rating` - Sort by rating, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    def get_sort_key(movie):
        if sort == movie_sort_options.movie_title:
            return movie['movie_title']
        elif sort == movie_sort_options.year:
            return movie['year']
        elif sort == movie_sort_options.rating:
            return -movie['imdb_rating']

    # retrieve movies from database
    movies = []
    for movie_id, movie_data in db.movies.items():
        if name.lower() in movie_data['title'].lower():
            movie = {
                "movie_id": int(movie_id),
                "movie_title": movie_data["title"] or None,
                "year": movie_data["year"] or None,
                "imdb_rating": float(movie_data['imdb_rating']),
                "imdb_votes": int(movie_data['imdb_votes'])
            }
            movies.append(movie)

    # sort and paginate 
    movies = sorted(movies, key=get_sort_key)
    movies = movies[offset : offset + limit]

    return movies
