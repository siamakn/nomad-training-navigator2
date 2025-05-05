# services/json_file_backend.py

import json
from pathlib import Path
from config.settings import settings
from datetime import datetime

class JSONFileBackend:
    def __init__(self):
        self.data_dir = settings.DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, resource: dict, filename: str) -> str:
        filepath = self.data_dir / f"{filename}.jsonld"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(resource, f, indent=2, ensure_ascii=False, default=str)
        return filename

    def load(self, filename: str) -> dict:
        filepath = self.data_dir / f"{filename}.jsonld"
        if not filepath.exists():
            raise FileNotFoundError(f"Metadata file not found: {filepath}")
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)

    def delete(self, filename: str) -> None:
        filepath = self.data_dir / f"{filename}.jsonld"
        if filepath.exists():
            filepath.unlink()

    def list_all(self) -> list[dict]:
        entries = []
        for file in self.data_dir.glob("*.jsonld"):
            with open(file, encoding="utf-8") as f:
                entries.append(json.load(f))
        return entries
