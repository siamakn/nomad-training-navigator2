# models/resource_metadata.py

from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import date


class ResourceMetadata(BaseModel):
    id: str
    type: str = "schema:LearningResource"
    title: str
    description: str
    subject: List[str]
    keywords: List[str]
    created: date
    date_modified: date
    educational_level: List[str]
    instructional_method: List[str]
    learning_resource_type: List[str]
    format: List[str]
    license: List[str]  # URLs as strings
    identifier: str  # Can be a DOI or regular URL string
    language: Optional[str] = "en"
    is_based_on: Optional[List[str]] = []
