from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class ResourceMetadata(BaseModel):
    id: str = Field(..., description="Unique identifier (URN UUID).")
    type: str = Field(default="schema:LearningResource")
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
    license: str
    identifier: str
    language: str = "en"
    is_based_on: Optional[str] = None

    class Config:
        from_attributes = True
