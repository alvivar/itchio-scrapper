import json


def js(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)
