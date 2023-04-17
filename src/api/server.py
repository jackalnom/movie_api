from fastapi import FastAPI
<<<<<<< HEAD
from src.api import characters, movies, pkg_util, lines
=======
from src.api import characters, movies, conversations, pkg_util
>>>>>>> db993774e9cc922cd0a443a79a1314fde568e413

description = """
Movie API returns dialog statistics on top hollywood movies from decades past.

## Characters

You can:
* **list characters with sorting and filtering options.**
* **retrieve a specific character by id**

## Movies

You can:
* **list movies with sorting and filtering options.**
* **retrieve a specific movie by id**
"""
tags_metadata = [
    {
        "name": "characters",
        "description": "Access information on characters in movies.",
    },
    {
        "name": "movies",
        "description": "Access information on top-rated movies.",
    },
]

app = FastAPI(
    title="Movie API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Quinn Peterson",
        "email": "qpeterso@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(characters.router)
app.include_router(movies.router)
app.include_router(pkg_util.router)
<<<<<<< HEAD
app.include_router(lines.router)
=======
app.include_router(conversations.router)
>>>>>>> db993774e9cc922cd0a443a79a1314fde568e413


@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API. See /docs for more information."}
