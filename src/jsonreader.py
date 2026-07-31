import json

def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)
    