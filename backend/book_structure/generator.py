"""
Book structure generator class.

This module implements the main logic for generating book structures
with the required hierarchy and validation rules.
"""

from typing import Dict, Any
from .models import Book, Module, Chapter, Topic
from . import naming


class BookStructureGenerator:
    """Generates book structures with modules, chapters, and topics."""

    def __init__(self):
        """Initialize the generator."""
        pass

    def generate_structure(self, subject: str) -> Book:
        """
        Generate a complete book structure with validation.

        Args:
            subject: The subject/topic of the book

        Returns:
            Book instance with generated structure

        Raises:
            ValueError: If the generated structure doesn't meet validation requirements
            TypeError: If the subject is not a string
        """
        if not isinstance(subject, str):
            raise TypeError(f"Subject must be a string, got {type(subject).__name__}")

        if not subject.strip():
            raise ValueError("Subject cannot be empty or contain only whitespace")

        try:
            # Generate names using the naming module
            names_data = naming.generate_book_structure_names(subject.strip())

            # Validate the generated structure meets requirements
            if len(names_data["modules"]) != 5:
                raise ValueError(
                    f"Generated {len(names_data['modules'])} modules, expected exactly 5"
                )

            # Create the modules with their chapters and topics
            modules = []
            for i, module_data in enumerate(names_data["modules"]):
                if not (5 <= len(module_data["chapters"]) <= 10):
                    raise ValueError(
                        f"Module {i+1} ('{module_data['name']}') has {len(module_data['chapters'])} chapters, "
                        f"expected between 5 and 10"
                    )

                chapters = []
                for j, chapter_data in enumerate(module_data["chapters"]):
                    if not (12 <= len(chapter_data["topics"]) <= 20):
                        raise ValueError(
                            f"Chapter {j+1} ('{chapter_data['name']}') in module {i+1} ('{module_data['name']}') "
                            f"has {len(chapter_data['topics'])} topics, expected between 12 and 20"
                        )

                    topics = []
                    for k, topic_name in enumerate(chapter_data["topics"]):
                        # Check for empty topic names
                        if not topic_name or not topic_name.strip():
                            raise ValueError(
                                f"Topic {k+1} in chapter {j+1} ('{chapter_data['name']}') "
                                f"in module {i+1} ('{module_data['name']}') has an empty name"
                            )
                        topics.append(Topic(name=topic_name))

                    # Check for duplicate topic names within a chapter
                    topic_names = [topic.name for topic in topics]
                    if len(set(topic_names)) != len(topic_names):
                        # Find the duplicate names
                        seen = set()
                        duplicates = []
                        for name in topic_names:
                            if name in seen:
                                if name not in duplicates:
                                    duplicates.append(name)
                            else:
                                seen.add(name)
                        raise ValueError(
                            f"Chapter '{chapter_data['name']}' in module '{module_data['name']}' "
                            f"has duplicate topic names: {duplicates}"
                        )

                    chapter = Chapter(name=chapter_data["name"], topics=topics)
                    chapters.append(chapter)

                module = Module(name=module_data["name"], chapters=chapters)
                modules.append(module)

            # Create and return the Book instance
            book = Book(subject=subject.strip(), modules=modules)
            return book

        except ValueError:
            # Re-raise ValueError as is since it's a validation error
            raise
        except Exception as e:
            # For any other unexpected errors, wrap with context
            raise ValueError(
                f"Unexpected error during book structure generation: {str(e)}"
            ) from e

    def generate_structure_with_validation(self, subject: str) -> Dict[str, Any]:
        """
        Generate a book structure and return validation results.

        Args:
            subject: The subject/topic of the book

        Returns:
            Dictionary containing the book structure and validation results
        """
        try:
            book = self.generate_structure(subject)

            # Validate the structure
            validation_results = {
                "valid": True,
                "errors": [],
                "summary": {
                    "subject": book.subject,
                    "module_count": len(book.modules),
                    "chapters_per_module": [len(m.chapters) for m in book.modules],
                    "topics_per_chapter": [
                        [len(c.topics) for c in m.chapters] for m in book.modules
                    ],
                },
            }

            # Validate module count
            if len(book.modules) != 5:
                validation_results["valid"] = False
                validation_results["errors"].append(
                    f"Expected exactly 5 modules, got {len(book.modules)}"
                )

            # Validate chapter counts per module
            for i, module in enumerate(book.modules):
                if not (5 <= len(module.chapters) <= 10):
                    validation_results["valid"] = False
                    validation_results["errors"].append(
                        f"Module {i+1} ({module.name}) has {len(module.chapters)} chapters, "
                        f"expected between 5 and 10"
                    )

            # Validate topic counts per chapter
            for i, module in enumerate(book.modules):
                for j, chapter in enumerate(module.chapters):
                    if not (12 <= len(chapter.topics) <= 20):
                        validation_results["valid"] = False
                        validation_results["errors"].append(
                            f"Chapter {j+1} in module {i+1} ({chapter.name}) has {len(chapter.topics)} topics, "
                            f"expected between 12 and 20"
                        )

            return {"book": book, "validation": validation_results}

        except Exception as e:
            return {
                "book": None,
                "validation": {
                    "valid": False,
                    "errors": [f"Generation error: {str(e)}"],
                },
            }

    def validate_structure(self, book: Book) -> Dict[str, Any]:
        """
        Validate an existing book structure.

        Args:
            book: Book instance to validate

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "valid": True,
            "errors": [],
            "summary": {
                "subject": book.subject,
                "module_count": len(book.modules),
                "chapters_per_module": [len(m.chapters) for m in book.modules],
                "topics_per_chapter": [
                    [len(c.topics) for c in m.chapters] for m in book.modules
                ],
            },
        }

        # Validate module count
        if len(book.modules) != 5:
            validation_results["valid"] = False
            validation_results["errors"].append(
                f"Expected exactly 5 modules, got {len(book.modules)}"
            )

        # Validate chapter counts per module
        for i, module in enumerate(book.modules):
            if not (5 <= len(module.chapters) <= 10):
                validation_results["valid"] = False
                validation_results["errors"].append(
                    f"Module {i+1} ({module.name}) has {len(module.chapters)} chapters, "
                    f"expected between 5 and 10"
                )

        # Validate topic counts per chapter
        for i, module in enumerate(book.modules):
            for j, chapter in enumerate(module.chapters):
                if not (12 <= len(chapter.topics) <= 20):
                    validation_results["valid"] = False
                    validation_results["errors"].append(
                        f"Chapter {j+1} in module {i+1} ({chapter.name}) has {len(chapter.topics)} topics, "
                        f"expected between 12 and 20"
                    )

        return validation_results

    def serialize_to_json(self, book: Book, indent: int = 2) -> str:
        """
        Serialize a book structure to JSON format.

        Args:
            book: Book instance to serialize
            indent: Number of spaces for JSON indentation (default 2)

        Returns:
            JSON string representation of the book structure
        """
        if book is None:
            raise ValueError("Cannot serialize None book object")

        # Convert the Pydantic model to a dictionary and then to JSON
        book_dict = book.dict()
        import json

        return json.dumps(book_dict, indent=indent, ensure_ascii=False)
