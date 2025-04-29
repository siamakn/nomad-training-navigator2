# utils/helpers.py

import json
from pathlib import Path
from config.settings import settings


def generate_uuid() -> str:
    from uuid import uuid4
    return str(uuid4())


def load_vocabulary() -> dict:
    vocab_path = Path("config/vocabulary.json")
    if not vocab_path.exists():
        raise FileNotFoundError("Vocabulary file not found.")
    return json.loads(vocab_path.read_text(encoding="utf-8"))


def save_vocabulary(vocab: dict) -> None:
    vocab_path = Path("config/vocabulary.json")
    vocab_path.write_text(json.dumps(vocab, indent=2, ensure_ascii=False))
