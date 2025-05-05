# services/json_file_backend.py

import json
from pathlib import Path
from config.settings import settings
from utils.logger import logger


class JSONFileBackend:
    def __init__(self):
        self.data_dir = settings.DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, resource: dict) -> str:
        resource_id = resource.get("@id")
        if not resource_id:
            raise ValueError("Resource must contain an '@id' field.")

        file_path = self.data_dir / f"{resource_id}.jsonld"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(resource, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved resource to {file_path}")
        return resource_id

    def load(self, resource_id: str) -> dict:
        file_path = self.data_dir / f"{resource_id}.jsonld"
        if not file_path.exists():
            raise FileNotFoundError(f"No metadata found with ID: {resource_id}")
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)

    def delete(self, resource_id: str) -> None:
        file_path = self.data_dir / f"{resource_id}.jsonld"
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted metadata file: {file_path}")

    def list_all(self) -> list[dict]:
        resources = []
        for file_path in self.data_dir.glob("*.jsonld"):
            with open(file_path, encoding="utf-8") as f:
                resources.append(json.load(f))
        return resources
