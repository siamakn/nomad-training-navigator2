# config/vocabulary_loader.py

import json
from pathlib import Path
from config.settings import settings


def load_vocabulary():
    vocab_path = Path(settings.DATA_DIR).parents[1] / "config" / "vocabulary.json"
    with open(vocab_path, encoding="utf-8") as f:
        return json.load(f)