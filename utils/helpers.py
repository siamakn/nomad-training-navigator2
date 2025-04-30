# utils/helpers.py

import uuid
import json
from pathlib import Path
from config.settings import settings

def generate_uuid():
    return str(uuid.uuid4())

def load_vocabulary():
    vocab_path = Path("config") / "vocabulary.json"
    with open(vocab_path, encoding="utf-8") as f:
        return json.load(f)

def save_vocabulary(vocab: dict):
    vocab_path = Path("config") / "vocabulary.json"
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, indent=2, ensure_ascii=False)
