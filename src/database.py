import csv
from dataclasses import dataclass

# TODO: You will want to replace all of the code below. It is just to show you
# an example of reading the CSV files where you will get the data to complete
# the assignment.

print("reading movies")

@dataclass
class Movie:
    movie_id: int
    title: str
    year: str
    imdb_rating: float
    imdb_votes: int
    raw_script_url: str

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    movies = []
    # moviesWithLines will contain the following information: it will be a dictionary whose keys are all
    # different movie_ids, for each movie_id there will be a list containing the Movie object and a dictionary
    # whose keys will be character_ids of characters with lines in this movie and whose values are the number of
    # lines they had
    moviesWithLines = {}
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        movie = Movie(int(row['movie_id']), row['title'], row['year'], float(row['imdb_rating']),
                      int(row['imdb_votes']), row['raw_script_url'])
        movies.append(movie)
        moviesWithLines[movie.movie_id] = [movie, {}]

@dataclass
class Character:
    character_id: int
    name: str
    movie_id: int
    gender: str
    age: int

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    characters = []
    # charsWithConvos will contain the following information: it will be a dictionary whose keys are
    # all different character_ids, for each character_id there will be a list containing the Character object,
    # a dictionary whose keys will be character_ids that this character has had conversations with and whose values
    # are the number of lines between these characters, and an int that represents this character's individual lines
    charsWithConvos = {}
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        genderRow = row['gender'] if row['gender'] else None
        ageRow = int(row['age']) if row['age'] else None
        character = Character(int(row['character_id']), row['name'], int(row['movie_id']), genderRow, ageRow)
        characters.append(character)
        charsWithConvos[character.character_id] = [character, {}, 0]

@dataclass
class Conversation:
    conversation_id: int
    character1_id: int
    character2_id: int
    movie_id: int

with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    conversations = []
    convoDictByID = {}
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        conversation = Conversation(int(row['conversation_id']), int(row['character1_id']), int(row['character2_id']),
                                    int(row['movie_id']))
        conversations.append(conversation)
        convoDictByID[conversation.conversation_id] = conversation

@dataclass
class Line:
    line_id: int
    character_id: int
    movie_id: int
    conversation_id: int
    line_sort: int
    line_text: str

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    lines = []
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        line = Line(int(row['line_id']), int(row['character_id']), int(row['movie_id']), int(row['conversation_id']),
                    int(row['line_sort']), row['line_text'])
        lines.append(line)
        charsWithConvos[line.character_id][2] += 1
        if line.character_id in moviesWithLines[line.movie_id][1]:
            moviesWithLines[line.movie_id][1][line.character_id] += 1
        else:
            moviesWithLines[line.movie_id][1][line.character_id] = 1
        currentConvo = convoDictByID[line.conversation_id]
        if currentConvo.character1_id in charsWithConvos[currentConvo.character2_id][1]:
            charsWithConvos[currentConvo.character1_id][1][currentConvo.character2_id] += 1
            charsWithConvos[currentConvo.character2_id][1][currentConvo.character1_id] += 1
        else:
            charsWithConvos[currentConvo.character1_id][1][currentConvo.character2_id] = 1
            charsWithConvos[currentConvo.character2_id][1][currentConvo.character1_id] = 1
