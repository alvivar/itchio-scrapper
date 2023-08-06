from tinydb import Query, TinyDB


db = TinyDB("db.json")


def upsert(games):
    Author = Query()

    for game in games:
        author = game.pop("author")
        author_url = game.pop("author_url")
        db_author = db.get(Author.url == author_url)

        if db_author:
            if not any(db_game["url"] == game["url"] for db_game in db_author["games"]):
                db_author["games"].append(game)
            data = {"games": db_author["games"]}
        else:
            data = {"author": author, "url": author_url, "games": [game]}

        db.upsert(data, Author.url == author_url)
