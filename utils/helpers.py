# utils/helpers.py

import uuid
import json
import re
from pathlib import Path
from config.settings import settings
from datetime import date


def generate_uuid() -> str:
    return str(uuid.uuid4())


def load_vocabulary() -> dict:
    vocab_path = Path("config") / "vocabulary.json"
    with open(vocab_path, encoding="utf-8") as f:
        return json.load(f)


def save_vocabulary(vocab: dict) -> None:
    vocab_path = Path("config") / "vocabulary.json"
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, indent=2, ensure_ascii=False)


def generate_filename(metadata) -> str:
    date_part = metadata.date_modified.strftime("%Y%m%d") if metadata.date_modified else "no_date"
    title_part = metadata.title.strip().lower()
    title_part = re.sub(r"[^a-z0-9 ]", "", title_part)
    title_part = "_".join(title_part.split()[:20])
    return f"{date_part}_{title_part}"
