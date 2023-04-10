import csv

# TODO: You will want to replace all of the code below. It is just to show you
# an example of reading the CSV files where you will get the data to complete
# the assignment.

print("reading movies")

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    movies = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]
    
with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    characters = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]

with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    conversations = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    lines = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]

    lines_by_character = []
    for line in lines:
        for character in lines_by_character:
            if line["character_id"] == character["character_id"]:
                character["character_id"] += 1
            else:
                for entry in characters:
                    if entry["character_id"] == line["character_id"]:
                        name = entry["name"]
                    else:
                        name = None
                newCharacter = {
                    "character_id" : line["character_id"],
                    "name" : name,
                    "num_lines" : 1,
                    "movie_id" : line["movie_id"]
                }
                lines_by_character.append(newCharacter)
    lines_by_character.sort(reverse=True, key= lambda x: x["num_lines"])
    lines_by_character.sort(reverse=True, key= lambda x: x["movie_id"])
    
    top_chars_by_movie = []
    for movie in movies:
        entry = { 
            "movie_id": movie["movie_id"],
            "top_chars" : filter(lambda x: x["movie_id"] 
               == movie["movie_id"], lines_by_character)
            }


