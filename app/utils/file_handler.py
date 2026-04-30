import json
import os

FILE_PATH = "app/data/logs.json"

def read_logs():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def write_logs(logs):
    with open(FILE_PATH, "w") as f:
        json.dump(logs, f, indent=2)