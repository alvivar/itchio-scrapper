import json
import os
import pytumblr
import env


env.load(".env")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
OAUTH_SECRET = os.environ.get("OAUTH_SECRET")


def dump(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


def get_all_posts(tumblr_client, blogName):
    offset = 0
    limit = 20

    games = []
    while True:
        posts = tumblr_client.posts(blogName, limit=limit, offset=offset)
        posts = posts["posts"]

        for post in posts:
            game = {
                "id_string": post["id_string"],
                "post_url": post["post_url"],
                "summary": post["summary"],
                "tags": post["tags"],
            }

            games.append(game)

        if len(posts) < limit:
            break

        offset += limit

    return games


if __name__ == "__main__":
    tumblr = pytumblr.TumblrRestClient(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        OAUTH_TOKEN,
        OAUTH_SECRET,
    )

    blogName = "bestgamesintheplanet"

    # tumblr.edit_post(blogName, id=618837499726446592, type="photo", tags=[])
    # info = tumblr.info()
    # dump(info, "tumblr.info.json")
