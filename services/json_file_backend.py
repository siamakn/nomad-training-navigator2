# services/json_file_backend.py

import json
from pathlib import Path
from typing import Dict, Any
from uuid import uuid4
from services.storage_interface import StorageBackend
from config.settings import settings


class JSONFileBackend(StorageBackend):
    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, resource: Dict[str, Any]) -> str:
        resource_id = resource.get("@id") or str(uuid4())
        resource["@id"] = resource_id
        file_path = self.data_dir / f"{resource_id}.jsonld"
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(resource, f, indent=2, ensure_ascii=False)
        return resource_id

    def load(self, resource_id: str) -> Dict[str, Any]:
        file_path = self.data_dir / f"{resource_id}.jsonld"
        if not file_path.exists():
            raise FileNotFoundError(f"No resource with ID {resource_id}")
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def list_all(self) -> list[Dict[str, Any]]:
        resources = []
        for file_path in self.data_dir.glob("*.jsonld"):
            with file_path.open("r", encoding="utf-8") as f:
                resources.append(json.load(f))
        return resources

    def delete(self, resource_id: str) -> None:
        file_path = self.data_dir / f"{resource_id}.jsonld"
        if file_path.exists():
            file_path.unlink()
