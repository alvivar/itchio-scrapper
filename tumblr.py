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


if __name__ == "__main__":
    tumblr = pytumblr.TumblrRestClient(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        OAUTH_TOKEN,
        OAUTH_SECRET,
    )

    info = tumblr.info()
    dump(info, "tumblr.info.json")

    bestgames = tumblr.posts("bestgamesintheplanet")
    dump(bestgames, "tumblr.bestgamesintheplanet.json")
