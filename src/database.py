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

    character_by_id = dict()
    gender_by_id = dict()
    for character in characters:
        key = str(character["character_id"])
        gender = character["gender"]
        character_by_id.__setitem__(key, character["name"])
        if gender == "":
            gender = None
        gender_by_id.__setitem__(key, gender)

    movie_by_id = {}
    for movie in movies:
        movie_by_id[movie["movie_id"]] = movie["title"]

    char_lines = {}
    for character in character_by_id:
        char_lines[character] = 0

    for line in lines:
        current_character = line["character_id"]
        char_lines[current_character] = char_lines[current_character] + 1

    lines_by_character = []
    for character in characters:
        name = character_by_id[character["character_id"]]
        newCharacter = {
            "character" : name,
            "character_id" : int(character["character_id"]),
            "num_lines" : int(char_lines[character["character_id"]]),
            "movie_id" : character["movie_id"]
        }
        lines_by_character.append(newCharacter)
    lines_by_character.sort(reverse=True, key= lambda x: x["num_lines"])
    lines_by_character.sort(reverse=True, key= lambda x: x["movie_id"])

    top_chars_by_movie = {}
    entry = []
    for movie in movies:
        entry = list(filter(lambda x: x["movie_id"] == movie["movie_id"],
                            lines_by_character))
        del entry[5:]
        top_chars_by_movie[movie["movie_id"]] = entry
