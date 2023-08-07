import os
import re
from datetime import datetime
from urllib.parse import urlparse, urlunparse

import requests
from playwright.sync_api import sync_playwright

import dump


SCRAPS_DIR = "scraps"
THUMBNAILS_DIR = "thumbnails"
os.makedirs(SCRAPS_DIR, exist_ok=True)
os.makedirs(THUMBNAILS_DIR, exist_ok=True)


def download(image_url, filename):
    response = requests.get(image_url)
    with open(filename, "wb") as f:
        f.write(response.content)


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
    cleaned = urlunparse((scheme, netloc, path, "", "", ""))

    return cleaned


def clean_name(name):
    name = re.sub(r"[^\w\-.]|[\s]", "_", name)
    name = re.sub(r"__+", "_", name)

    return name


def get_games_from(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
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

            print(f"Found: {url}")

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
                    "thumbnail_url": thumbnail,
                    "web": web_flag,
                    "windows": windows_flag,
                    "linux": linux_flag,
                    "apple": apple_flag,
                    "android": android_flag,
                }
            )

        return games


def download_images(games, path):
    for game in games:
        url = game["thumbnail_url"]
        if url:
            filename = clean_name(url)
            download(url, f"{path}/{filename}")
            game["thumbnail_file"] = filename
            print(f"Downloaded: {url}")

    return games


def extract_game_info(games, dump_file=False):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        browser.new_context(viewport={"width": 1920, "height": 1080})
        page = browser.new_page()

        for game in games:
            url = game["url"]
            page.goto(url)

            print(f"Extracting game info: {url}")

            # Price
            original_price = page.query_selector(".original_price")
            price = page.query_selector('span.dollars[itemprop="price"]')

            original_price = original_price.inner_text() if original_price else None
            price = price.inner_text() if price else None

            game["price"] = original_price or price or 0

            # Tags
            tags_cell = page.query_selector('td:has-text("Tags") + td')
            if not tags_cell:
                continue

            tag_elements = tags_cell.query_selector_all("a")
            tags = [tag_element.inner_text() for tag_element in tag_elements]
            game["tags"] = tags

        if dump_file:
            time = datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
            dump.js(games, f"{SCRAPS_DIR}/itch.games.{time}.json")

        return games


if __name__ == "__main__":
    games = get_games_from("https://itch.io/games/top-rated/last-30-days")
    # dump.js(games, "itch.games.json")

    games = download_images(games, THUMBNAILS_DIR)
    # dump.js(games, "itch.games.images.json")

    games_tagged = extract_game_info(games, dump_file=True)
    # dump.js(games, "itch.games.info.json")
