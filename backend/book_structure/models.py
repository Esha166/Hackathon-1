"""
Pydantic models for book structure generation.

This module defines the data models for Book, Module, Chapter, and Topic
with appropriate validation rules as specified in the requirements.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class Topic(BaseModel):
    """Represents a topic within a chapter."""

    name: str = Field(
        ...,
        description="The realistic name/title of the topic based on potential subject matter",
    )
    description: Optional[str] = Field(
        None, description="A brief description of the topic"
    )

    @validator("name")
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Topic name must not be empty")
        return v.strip()


class Chapter(BaseModel):
    """Represents a chapter within a module."""

    name: str = Field(
        ...,
        description="The descriptive name/title of the chapter based on potential content",
    )
    topics: List[Topic] = Field(
        ...,
        min_items=12,
        max_items=20,
        description="A list of topics contained in the chapter",
    )
    description: Optional[str] = Field(
        None, description="A brief description of the chapter"
    )

    @validator("name")
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Chapter name must not be empty")
        return v.strip()

    @validator("topics")
    def validate_topics(cls, v):
        if len(v) < 12 or len(v) > 20:
            raise ValueError(
                "Chapter must contain between 12 and 20 topics (inclusive)"
            )

        # Check for unique topic names within the chapter
        topic_names = [topic.name for topic in v]
        if len(set(topic_names)) != len(topic_names):
            raise ValueError("All topic names must be unique within the chapter")

        return v


class Module(BaseModel):
    """Represents a module within a book."""

    name: str = Field(
        ...,
        description="The descriptive name/title of the module based on potential content",
    )
    chapters: List[Chapter] = Field(
        ...,
        min_items=5,
        max_items=10,
        description="A list of chapters contained in the module",
    )
    description: Optional[str] = Field(
        None, description="A brief description of the module"
    )

    @validator("name")
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Module name must not be empty")
        return v.strip()

    @validator("chapters")
    def validate_chapters(cls, v):
        if len(v) < 5 or len(v) > 10:
            raise ValueError(
                "Module must contain between 5 and 10 chapters (inclusive)"
            )
        return v


class Book(BaseModel):
    """Represents a complete book structure."""

    subject: str = Field(..., description="The subject/topic of the book")
    modules: List[Module] = Field(
        ...,
        min_items=5,
        max_items=5,
        description="A list of modules in the book structure",
    )

    @validator("modules")
    def validate_modules(cls, v):
        if len(v) != 5:
            raise ValueError("Book must contain exactly 5 modules")
        return v
