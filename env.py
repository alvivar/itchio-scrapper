import os
import sys


ENV_CACHE = {}


def load(filepath):
    global ENV_CACHE

    frozen = getattr(sys, "frozen", False)  # Pyinstaller
    base_path = sys._MEIPASS if frozen else os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_path, filepath)

    if env_path not in ENV_CACHE:
        if os.path.exists(env_path):
            env = {}
            with open(env_path, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=")
                        env[key.strip()] = value.strip()

            ENV_CACHE[env_path] = env

    os.environ.update(ENV_CACHE[env_path])
