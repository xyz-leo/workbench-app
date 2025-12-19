# backend/todo/storage.py

"""
Handles reading and writing the tasks/workspaces JSON.
"""

import json
from pathlib import Path
from backend.utils.file_lock import FileLock

DATA_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "todo.json"
DATA_FILE.parent.mkdir(exist_ok=True)  # garante que a pasta 'data' existe

def load_data():
    """Load the JSON data from file. Return empty dict if file doesn't exist."""
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Save JSON data to file safely using a file lock."""
    lock = FileLock(str(DATA_FILE))
    with lock:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

