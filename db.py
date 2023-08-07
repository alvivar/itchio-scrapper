from tinydb import Query, TinyDB


db = TinyDB("data/db.json")


def upsert(games):
    Author = Query()

    for game in games:
        author = game.pop("author")
        author_url = game.pop("author_url")
        db_author = db.get(Author.url == author_url)

        if db_author:
            game_index = next(
                (
                    index
                    for index, db_game in enumerate(db_author["games"])
                    if db_game["url"] == game["url"]
                ),
                None,
            )

            if game_index is not None:
                db_author["games"][game_index] = game
            else:
                db_author["games"].append(game)

            data = {"games": db_author["games"]}
        else:
            data = {"author": author, "url": author_url, "games": [game]}

        db.upsert(data, Author.url == author_url)
