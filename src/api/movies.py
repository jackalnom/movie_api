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
    for movie in db.movies:
        if movie["movie_id"] == id:
             json = {
                "movie_id" : movie["movie_id"],
                "title" : movie["title"],
                "top_characters" : 
                filter(lambda x: x["movie_id"] == id, db.top_chars_by_movie)
            }
        else:
            json = None

    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return json


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
    filtered_movies = filter(lambda x: name in x["movie_title"], db.movies)
    movies = []
    new_movie = {}

    if name != "":
        movie_list = filter(lambda x: str in x["title"], filtered_movies)
    else:
        movie_list = filtered_movies
    for i in range(offset, limit):
        if i < len(filtered_movies):
            new_movie = {
                "movie_id" : filtered_movies[i]["movie_id"],
                "movie_title" : filtered_movies[i]["movie_title"],
                "year" : filtered_movies[i]["year"],
                "imdb_rating" : filtered_movies[i]["imdb_rating"],
                "imdb_votes" : filtered_movies[i]["imdb_votes"]
            }
            movies.append(new_movie)

    return movies
