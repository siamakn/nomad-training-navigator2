# services/metadata_manager.py

from models.resource_metadata import ResourceMetadata
from utils.logger import logger
from config.settings import settings
from services.json_file_backend import JSONFileBackend
from datetime import date
import json


class MetadataManager:
    backend = JSONFileBackend()

    @staticmethod
    def save_metadata(metadata: ResourceMetadata) -> str:
        """Save metadata using the configured backend."""
        data = MetadataManager._to_jsonld(metadata)
        resource_id = MetadataManager.backend.save(data)
        logger.info(f"Metadata saved: {resource_id}")
        return resource_id

    @staticmethod
    def load_metadata(metadata_id: str) -> ResourceMetadata:
        """Load metadata using the configured backend."""
        data = MetadataManager.backend.load(metadata_id)
        metadata = MetadataManager._from_jsonld(data)
        logger.info(f"Metadata loaded: {metadata_id}")
        return metadata

    @staticmethod
    def list_metadata() -> list[ResourceMetadata]:
        """List all metadata resources."""
        all_data = MetadataManager.backend.list_all()
        return [MetadataManager._from_jsonld(d) for d in all_data]

    @staticmethod
    def delete_metadata(metadata_id: str) -> None:
        """Delete a metadata resource."""
        MetadataManager.backend.delete(metadata_id)
        logger.info(f"Metadata deleted: {metadata_id}")

    @staticmethod
    def _to_jsonld(metadata: ResourceMetadata) -> dict:
        """Convert ResourceMetadata instance to JSON-LD structure."""
        return {
            "@context": "context/context.jsonld",
            "@id": metadata.id,
            "@type": metadata.type,
            "dct:title": metadata.title,
            "dct:description": metadata.description,
            "dct:subject": metadata.subject,
            "schema:keywords": metadata.keywords,
            "schema:dateCreated": metadata.created.isoformat(),
            "schema:dateModified": metadata.date_modified.isoformat(),
            "schema:educationalLevel": metadata.educational_level,
            "dct:instructionalMethod": metadata.instructional_method,
            "schema:learningResourceType": metadata.learning_resource_type,
            "schema:encodingFormat": metadata.format,
            "schema:license": [str(l) for l in metadata.license],
            "schema:identifier": str(metadata.identifier),
            "schema:inLanguage": metadata.language,
            "schema:isBasedOn": [str(u) for u in metadata.is_based_on] if metadata.is_based_on else []
        }

    @staticmethod
    def _from_jsonld(data: dict) -> ResourceMetadata:
        """Convert JSON-LD structure to ResourceMetadata instance."""
        return ResourceMetadata(
            id=data["@id"],
            type=data.get("@type", "schema:LearningResource"),
            title=data["dct:title"],
            description=data["dct:description"],
            subject=data["dct:subject"],
            keywords=data["schema:keywords"],
            created=date.fromisoformat(data["schema:dateCreated"]),
            date_modified=date.fromisoformat(data["schema:dateModified"]),
            educational_level=data["schema:educationalLevel"],
            instructional_method=data["dct:instructionalMethod"],
            learning_resource_type=data["schema:learningResourceType"],
            format=data["schema:encodingFormat"],
            license=data["schema:license"],
            identifier=data["schema:identifier"],
            language=data.get("schema:inLanguage", "en"),
            is_based_on=data.get("schema:isBasedOn", [])
        )
