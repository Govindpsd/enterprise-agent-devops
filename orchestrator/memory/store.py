# orchestrator/memory/store.py

import json
import os

MEMORY_FILE = "incident_memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(entry):
    memory = load_memory()
    memory.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def find_similar_incident(service):
    memory = load_memory()
    for entry in memory:
        if entry["service"] == service:
            return entry
    return None
