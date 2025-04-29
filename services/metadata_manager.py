from models.resource_metadata import ResourceMetadata
from utils.logger import logger
from config.settings import settings
from pathlib import Path
import json


class MetadataManager:
    @staticmethod
    def save_metadata(metadata: ResourceMetadata) -> None:
        """Save metadata as a JSON-LD file."""
        path = settings.DATA_DIR / f"{metadata.id}.jsonld"
        data = MetadataManager._to_jsonld(metadata)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        logger.info(f"Metadata saved: {path}")

    @staticmethod
    def load_metadata(metadata_id: str) -> ResourceMetadata:
        """Load metadata from a JSON-LD file."""
        path = settings.DATA_DIR / f"{metadata_id}.jsonld"
        if not path.exists():
            logger.error(f"Metadata file not found: {path}")
            raise FileNotFoundError(f"No metadata found with id: {metadata_id}")
        data = json.loads(path.read_text())
        metadata = MetadataManager._from_jsonld(data)
        logger.info(f"Metadata loaded: {path}")
        return metadata

    @staticmethod
    def _to_jsonld(metadata: ResourceMetadata) -> dict:
        """Convert ResourceMetadata instance to JSON-LD structure."""
        return {
            "@context": {
                "dct": "http://purl.org/dc/terms/",
                "schema": "http://schema.org/",
                "id": "@id",
                "type": "@type"
            },
            "id": metadata.id,
            "type": metadata.type,
            "dct:title": metadata.title,
            "dct:description": metadata.description,
            "dct:subject": metadata.subject,
            "schema:keywords": metadata.keywords,
            "dct:created": metadata.created.isoformat(),
            "schema:dateModified": metadata.date_modified.isoformat(),
            "schema:educationalLevel": metadata.educational_level,
            "dct:instructionalMethod": metadata.instructional_method,
            "schema:learningResourceType": metadata.learning_resource_type,
            "dct:type": metadata.format,
            "schema:license": metadata.license,
            "schema:identifier": metadata.identifier,
            "schema:inLanguage": metadata.language,
            "schema:isBasedOn": metadata.is_based_on
        }

    @staticmethod
    def _from_jsonld(data: dict) -> ResourceMetadata:
        """Convert JSON-LD structure to ResourceMetadata instance."""
        return ResourceMetadata(
            id=data["id"],
            type=data.get("type", "schema:LearningResource"),
            title=data["dct:title"],
            description=data["dct:description"],
            subject=data["dct:subject"],
            keywords=data["schema:keywords"],
            created=date.fromisoformat(data["dct:created"]),
            date_modified=date.fromisoformat(data["schema:dateModified"]),
            educational_level=data["schema:educationalLevel"],
            instructional_method=data["dct:instructionalMethod"],
            learning_resource_type=data["schema:learningResourceType"],
            format=data["dct:type"],
            license=data["schema:license"],
            identifier=data["schema:identifier"],
            language=data.get("schema:inLanguage", "en"),
            is_based_on=data.get("schema:isBasedOn")
        )
