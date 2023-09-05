import json

import db
from itch import download_images, extract_game_info, get_games_from


def dump(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    games = get_games_from("https://itch.io/games/top-rated/last-30-days")
    dump(games, "last_itch.json")

    games = download_images(games, "thumbnails")
    dump(games, "last_itch_images.json")

    games_tagged = extract_game_info(games)
    dump(games, "last_itch_tagged.json")

    db.upsert(games)
