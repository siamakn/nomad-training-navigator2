# services/storage_interface.py

from abc import ABC, abstractmethod
from typing import Dict, Any


class StorageBackend(ABC):
    @abstractmethod
    def save(self, resource: Dict[str, Any]) -> str:
        """Save a resource. Returns the ID."""
        pass

    @abstractmethod
    def load(self, resource_id: str) -> Dict[str, Any]:
        """Load a resource by ID."""
        pass

    @abstractmethod
    def list_all(self) -> list[Dict[str, Any]]:
        """List all stored resources."""
        pass

    @abstractmethod
    def delete(self, resource_id: str) -> None:
        """Delete a resource by ID."""
        pass
