import json
import os
import sys
from datetime import datetime
from time import sleep
from playwright.sync_api import sync_playwright


frozen = getattr(sys, "frozen", False)  # Pyinstaller
base_path = sys._MEIPASS if frozen else os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_path, ".env")

if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key.strip()] = value.strip()


def get_inner_text(element):
    return element.inner_text() if element else None


with sync_playwright() as p:
    print("Starting")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://itch.io/games/top-rated/last-7-days")

    games = page.query_selector_all(".game_cell")

    for game in games:
        title = game.query_selector(".title").inner_text()
        description = game.query_selector(".game_text").inner_text()
        author = game.query_selector(".game_author").inner_text()
        genre = game.query_selector(".game_genre").inner_text()

        web_flag = game.query_selector(".web_flag") is not None
        windows_flag = game.query_selector('[class*="icon-windows"]') is not None
        linux_flag = game.query_selector(".icon-tux") is not None
        apple_flag = game.query_selector(".icon-apple") is not None
        android_flag = game.query_selector(".icon-android") is not None

        print(f"{title} - {description} - {author} - {genre}")
        print(
            f"Web: {web_flag}, Windows: {windows_flag}, Linux: {linux_flag}, Apple: {apple_flag}, Android: {android_flag}"
        )

    sleep(5)
