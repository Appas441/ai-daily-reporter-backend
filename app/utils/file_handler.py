import json
import os

FILE_PATH = "app/data/logs.json"


# ✅ Ensure folder exists
def ensure_file():
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)


# ✅ READ LOGS (SAFE)
def read_logs():
    ensure_file()

    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


# ✅ WRITE LOGS (SAFE)
def write_logs(logs):
    ensure_file()

    with open(FILE_PATH, "w") as f:
        json.dump(logs, f, indent=2)