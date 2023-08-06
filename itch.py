import json
from urllib.parse import urlparse, urlunparse
from playwright.sync_api import sync_playwright


def dump(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


def get_text(element):
    return element.inner_text() if element else ""


def get_image(element):
    return element.get_attribute("src") if element else ""


def get_url(element):
    return element.get_attribute("href") if element else ""


def clean_url(url):
    url_parts = urlparse(url)
    scheme = url_parts.scheme.lower()
    netloc = url_parts.netloc.lower().replace("www.", "")
    path = url_parts.path.rstrip("/")
    cleaned_url = urlunparse((scheme, netloc, path, "", "", ""))
    return cleaned_url


def get_games_from(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        browser.new_context(viewport={"width": 1920, "height": 1080})

        page = browser.new_page()
        page.goto(url)

        games = []
        for game in page.query_selector_all(".game_cell"):
            game.scroll_into_view_if_needed()
            page.wait_for_timeout(100)

            title = get_text(game.query_selector(".title"))
            description = get_text(game.query_selector(".game_text"))
            url = get_url(game.query_selector(".game_link"))

            author = get_text(game.query_selector(".game_author"))
            author_url = get_url(game.query_selector(".game_author a"))

            genre = get_text(game.query_selector(".game_genre"))
            thumbnail = get_image(game.query_selector(".thumb_link img"))

            web_flag = game.query_selector(".web_flag") is not None
            windows_flag = game.query_selector('[class*="icon-windows"]') is not None
            linux_flag = game.query_selector(".icon-tux") is not None
            apple_flag = game.query_selector(".icon-apple") is not None
            android_flag = game.query_selector(".icon-android") is not None

            games.append(
                {
                    "title": title,
                    "description": description,
                    "url": clean_url(url),
                    "author": author,
                    "author_url": clean_url(author_url),
                    "genre": genre,
                    "thumbnail": thumbnail,
                    "web": web_flag,
                    "windows": windows_flag,
                    "linux": linux_flag,
                    "apple": apple_flag,
                    "android": android_flag,
                }
            )

        browser.close()

        return games


if __name__ == "__main__":
    games = get_games_from("https://itch.io/games/top-rated/last-30-days")
    dump(games, "itch.debug.json")
