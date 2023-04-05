import csv

# TODO: You will want to replace all of the code below. It is just to show you
# an example of reading the CSV files where you will get the data to complete
# the assignment.

print("reading movies")

def create_dict_a(id_name, file):
    csv_reader = csv.DictReader(file, skipinitialspace=True)
    return { row[id_name]: row for row in csv_reader}

def create_dict_b(id_name, file):
    out = {}
    reader = csv.DictReader(file)
    for row in reader:
        id = row.pop(id_name)
        out[id] = row
    return out 

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    movies = create_dict_b("movie_id", csv_file)

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    characters = create_dict_b("character_id", csv_file)

with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    conversations = create_dict_b("conversation_id", csv_file)

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    lines = create_dict_b("line_id", csv_file)
