import csv
import json

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
            "imdb_votes": int(row["imdb_votes"])
        }
        movies.append(movie)

movie_list = []
for movie in movies:
    item = {
        "movie_id": movie["movie_id"],
        "movie_title": movie["title"],
        "year": movie["year"],
        "imdb_rating": movie["imdb_rating"],
        "imdb_votes": movie["imdb_votes"]
    }
    movie_list.append(item)

def get_title(movied_id:int):
    for movie in movies:
        if movie["movie_id"] == movied_id:
            return movie["title"]
    else:
        return None;

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

# gets counts of lines of each character stored in a kvp("character_id", "num_lines")
character_lines = {}
for line in lines:
    if line["character_id"] not in character_lines:
        character_lines[line["character_id"]] = 1
    else:
        character_lines[line["character_id"]] += 1

# gets counts of lines of each conversation stored in a kvp(conversation_id, number_of_lines)
conversation_lines = {}
for line in lines:
    if line["conversation_id"] not in conversation_lines:
        conversation_lines[line["conversation_id"]] = 1
    else:
        conversation_lines[line["conversation_id"]] += 1

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    characters = []
    for row in csv_reader:
        character = {
            "character_id": int(row["character_id"]),
            "name": row["name"],
            "movie_id": int(row["movie_id"]),
            "number_of_lines": 0 if int(row["character_id"]) not in character_lines else character_lines[int(row["character_id"])],
            "movie": get_title(int(row["movie_id"])),
            "gender": row["gender"] if len(row["gender"]) != 0 else None,
            "age": int(row["age"]) if row["age"].isdigit() else None
        }
        characters.append(character)

character_list = []
for character in characters:
    item = {
        "character_id": character["character_id"],
        "character": character["name"],
        "movie": character["movie"],
        "number_of_lines": character["number_of_lines"]
    }
    character_list.append(item)

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


'''
top_lines = {}
for character in characters:
    id = character["character_id"]
    for line in lines:
'''

# do a lot more indexing and preprocessing of data here (so you don't have to call multiple times)
# do it more for the list_characters and list_movies function.

#{character_id -> [{character_id, lines, movie}]}
