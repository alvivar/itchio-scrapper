import json
import os
import sys

import db
from itch import get_games_from, extract_game_info


frozen = getattr(sys, "frozen", False)  # Pyinstaller
base_path = sys._MEIPASS if frozen else os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_path, ".env")

if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key.strip()] = value.strip()


def dump(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    games = get_games_from("https://itch.io/games/top-rated/last-30-days")
    dump(games, "last_itch.json")

    games_tagged = extract_game_info(games)
    dump(games, "last_itch_tagged.json")

    db.upsert(games)
