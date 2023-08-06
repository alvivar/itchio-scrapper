import json
import db
from itch import get_games_from, extract_game_info


def dump(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    games = get_games_from("https://itch.io/games/top-rated/last-30-days")
    dump(games, "last_itch.json")

    games_tagged = extract_game_info(games)
    dump(games, "last_itch_tagged.json")

    db.upsert(games)
