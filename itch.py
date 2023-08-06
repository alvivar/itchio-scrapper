import json
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright


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


def get_text(element):
    return element.inner_text() if element else ""


def get_image(element):
    return element.get_attribute("src") if element else ""


def get_url(element):
    return element.get_attribute("href") if element else ""


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        browser.new_context(viewport={"width": 1920, "height": 1080})

        page = browser.new_page()
        page.goto("https://itch.io/games/top-rated/last-30-days")

        games_db = []

        games = page.query_selector_all(".game_cell")
        for game in games:
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

            games_db.append(
                {
                    "title": title,
                    "description": description,
                    "url": url,
                    "author": author,
                    "author_url": author_url,
                    "genre": genre,
                    "thumbnail": thumbnail,
                    "web": web_flag,
                    "windows": windows_flag,
                    "linux": linux_flag,
                    "apple": apple_flag,
                    "android": android_flag,
                }
            )

        dump(games_db, "last_itch.json")
