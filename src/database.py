import csv
import json

# TODO: You will want to replace all of the code below. It is just to show you
# an example of reading the CSV files where you will get the data to complete
# the assignment.

# added appropriate types to json tables, may abstract more

print("reading movies")

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    movies = []
    for row in csv_reader:
        movie = {
            "movie_id": int(row["movie_id"]),
            "title": row["title"],
            "year": row["year"],
            "imdb_rating": float(row["imdb_rating"]),
            "imdb_votes": int(row["imdb_votes"]),
            "raw_script_url": row["raw_script_url"]
        }
        movies.append(movie)

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    characters = []
    for row in csv_reader:
        character = {
            "character_id": int(row["character_id"]),
            "name": row["name"],
            "movie_id": int(row["movie_id"]),
            "gender": row["gender"] if len(row["gender"]) != 0 else None,
            "age": int(row["age"]) if row["age"].isdigit() else None
        }
        characters.append(character)

with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    conversations = []
    for row in csv_reader:
        conversation = {
            "conversation_id": int(row["conversation_id"]),
            "character1_id": int(row["character1_id"]),
            "character2_id": int(row["character2_id"]),
            "movie_id": int(row["movie_id"])
        }
        conversations.append(conversation)

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    lines = []
    for row in csv_reader:
        line = {
            "line_id": int(row["line_id"]),
            "character_id": int(row["character_id"]),
            "movie_id": int(row["movie_id"]),
            "conversation_id": int(row["conversation_id"]),
            "line_sort": int(row["line_sort"]),
            "line_text": str(row["line_text"])
        }
        lines.append(line)
