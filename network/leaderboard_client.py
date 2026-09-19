import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not configured in .env"
    )


client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["Cyber_Blitz"]

leaderboard = db["leaderboard"]


# One registered attempt per player per game.
leaderboard.create_index(
    [
        ("playerId", 1),
        ("gameId", 1)
    ],
    unique=True
)


def test_connection():

    client.admin.command("ping")

    return True


def calculate_unified_score(
    raw_score,
    gameplay_time,
    max_game_time=40.0
):

    if raw_score <= 0:
        return 0

    time_ratio = min(
        max(gameplay_time / max_game_time, 0.0),
        1.0
    )

    speed_bonus = round(
        9 * (1 - time_ratio)
    )

    unified_score = (
        raw_score * 10
        + speed_bonus
    )

    return unified_score


def submit_score(
    player_id,
    player_name,
    raw_score,
    gameplay_time,
    game_id="cyber_rapid_fire"
):
    print(
        "SUBMIT_SCORE CALLED:",
        player_id,
        player_name,
        raw_score,
        gameplay_time
    )


    unified_score = calculate_unified_score(
        raw_score,
        gameplay_time
    )

    document = {

        "playerId":
            player_id,

        "playerName":
            player_name,

        "score":
            unified_score,

        "gameId":
            game_id
    }

    try:

        result = leaderboard.insert_one(
            document
        )

        return {
            "registered": True,
            "score": unified_score,
            "inserted_id": str(
                result.inserted_id
            )
        }

    except DuplicateKeyError:

        return {
            "registered": False,
            "score": unified_score,
            "reason": "FIRST_ATTEMPT_ALREADY_REGISTERED"
        }