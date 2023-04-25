import csv
from src.datatypes import Character, Movie, Conversation, Line
import os
import io
from supabase import Client, create_client
import dotenv

# DO NOT CHANGE THIS TO BE HARDCODED. ONLY PULL FROM ENVIRONMENT VARIABLES.
dotenv.load_dotenv()
supabase_api_key = os.environ.get("SUPABASE_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")

if supabase_api_key is None or supabase_url is None:
    raise Exception(
        "You must set the SUPABASE_API_KEY and SUPABASE_URL environment variables."
    )

supabase: Client = create_client(supabase_url, supabase_api_key)

sess = supabase.auth.get_session()

# TODO: Below is purely an example of reading and then writing a csv from supabase.

# Reading in the log file from the supabase bucket
conversations_csv = (
    supabase.storage.from_("movie-api")
    .download("conversations.csv")
    .decode("utf-8")
)

convos = []
for row in csv.DictReader(io.StringIO(conversations_csv), skipinitialspace=True):
    convos.append(row)


# Writing to the log file and uploading to the supabase bucket
def upload_new_conversations():
    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output, fieldnames=["conversation_id","character1_id","character2_id","movie_id"]
    )
    csv_writer.writeheader()
    csv_writer.writerows(convos)
    supabase.storage.from_("movie-api").upload(
        "conversations.csv",
        bytes(output.getvalue(), "utf-8"),
        {"x-upsert": "true"},
    )

# Reading in the log file from the supabase bucket
lines_csv = (
    supabase.storage.from_("movie-api")
    .download("lines.csv")
    .decode("utf-8")
)

lin = []
for row in csv.DictReader(io.StringIO(lines_csv), skipinitialspace=True):
    lin.append(row)


# Writing to the log file and uploading to the supabase bucket
def upload_new_lines():
    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output, fieldnames=["line_id","character_id","movie_id","conversation_id","line_sort","line_text"]
    )
    csv_writer.writeheader()
    csv_writer.writerows(lin)
    supabase.storage.from_("movie-api").upload(
        "lines.csv",
        bytes(output.getvalue(), "utf-8"),
        {"x-upsert": "true"},
    )


def try_parse(type, val):
    try:
        return type(val)
    except ValueError:
        return None


with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    movies = {
        try_parse(int, row["movie_id"]): Movie(
            try_parse(int, row["movie_id"]),
            row["title"] or None,
            row["year"] or None,
            try_parse(float, row["imdb_rating"]),
            try_parse(int, row["imdb_votes"]),
            row["raw_script_url"] or None,
        )
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    }

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    characters = {}
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        char = Character(
            try_parse(int, row["character_id"]),
            row["name"] or None,
            try_parse(int, row["movie_id"]),
            row["gender"] or None,
            try_parse(int, row["age"]),
            0,
        )
        characters[char.id] = char

with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    maxConvoID = 0
    conversations = {}
    for row in csv.DictReader(io.StringIO(conversations_csv), skipinitialspace=True):
        currConvoID = try_parse(int, row["conversation_id"])
        if currConvoID is not None:
            if currConvoID > maxConvoID:
                maxConvoID = currConvoID
        conv = Conversation(
            currConvoID,
            try_parse(int, row["character1_id"]),
            try_parse(int, row["character2_id"]),
            try_parse(int, row["movie_id"]),
            0,
        )
        conversations[conv.id] = conv

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    maxLineID = 0
    lines = {}
    for row in csv.DictReader(io.StringIO(lines_csv), skipinitialspace=True):
        currLineID = try_parse(int, row["line_id"])
        if currLineID is not None:
            if currLineID > maxLineID:
                maxLineID = currLineID
        line = Line(
            currLineID,
            try_parse(int, row["character_id"]),
            try_parse(int, row["movie_id"]),
            try_parse(int, row["conversation_id"]),
            try_parse(int, row["line_sort"]),
            row["line_text"],
        )
        lines[line.id] = line
        c = characters.get(line.c_id)
        if c:
            c.num_lines += 1

        conv = conversations.get(line.conv_id)
        if conv:
            conv.num_lines += 1
