"""
Unit tests for the book structure generator.

This module contains tests for the BookStructureGenerator class.
"""
import sys
import os
import pytest

# Add the parent directory to the Python path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from book_structure.generator import BookStructureGenerator
from book_structure.models import Book


class TestBookStructureGenerator:
    """Tests for the BookStructureGenerator class."""

    def test_generator_initialization(self):
        """Test that the generator can be initialized."""
        generator = BookStructureGenerator()
        assert generator is not None

    def test_generate_structure_basic(self):
        """Test generating a basic book structure."""
        generator = BookStructureGenerator()
        book = generator.generate_structure("Test Subject")

        assert isinstance(book, Book)
        assert book.subject == "Test Subject"
        assert len(book.modules) == 5  # Exactly 5 modules required

        # Check that each module has the right number of chapters
        for module in book.modules:
            assert 5 <= len(module.chapters) <= 10  # Between 5-10 chapters per module

            # Check that each chapter has the right number of topics
            for chapter in module.chapters:
                assert 12 <= len(chapter.topics) <= 20  # Between 12-20 topics per chapter

    def test_generate_structure_with_validation(self):
        """Test generating a book structure with validation results."""
        generator = BookStructureGenerator()
        result = generator.generate_structure_with_validation("Test Subject")

        assert "book" in result
        assert "validation" in result

        book = result["book"]
        validation = result["validation"]

        assert isinstance(book, Book)
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0
        assert validation["summary"]["module_count"] == 5

        # Verify chapter counts per module
        for chapter_count in validation["summary"]["chapters_per_module"]:
            assert 5 <= chapter_count <= 10

        # Verify topic counts per chapter
        for chapter_topic_counts in validation["summary"]["topics_per_chapter"]:
            for topic_count in chapter_topic_counts:
                assert 12 <= topic_count <= 20

    def test_generate_structure_invalid_subject_type(self):
        """Test that generating with non-string subject raises an error."""
        generator = BookStructureGenerator()

        with pytest.raises(TypeError):
            generator.generate_structure(123)  # Should be string, not int

        with pytest.raises(TypeError):
            generator.generate_structure(None)  # Should be string, not None

    def test_generate_structure_empty_subject(self):
        """Test that generating with empty or whitespace-only subject raises an error."""
        generator = BookStructureGenerator()

        with pytest.raises(ValueError):
            generator.generate_structure("")

        with pytest.raises(ValueError):
            generator.generate_structure("   ")

    def test_validate_structure_valid(self):
        """Test validating a valid book structure."""
        generator = BookStructureGenerator()
        book = generator.generate_structure("Test Subject")

        validation = generator.validate_structure(book)
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0

    def test_validate_structure_invalid_module_count(self):
        """Test validating a book structure with wrong number of modules."""
        # Create a book with only 4 modules (should be 5)
        generator = BookStructureGenerator()
        book = generator.generate_structure("Test Subject")

        # Manually modify the book to have 4 modules (invalid)
        book.modules = book.modules[:4]

        validation = generator.validate_structure(book)
        assert validation["valid"] is False
        assert any("5 modules" in error for error in validation["errors"])

    def test_validate_structure_invalid_chapter_count(self):
        """Test validating a book structure with invalid chapter counts."""
        generator = BookStructureGenerator()
        book = generator.generate_structure("Test Subject")

        # Modify the first module to have only 4 chapters (should be 5-10)
        book.modules[0].chapters = book.modules[0].chapters[:4]

        validation = generator.validate_structure(book)
        assert validation["valid"] is False
        assert any("expected between 5 and 10" in error for error in validation["errors"])

    def test_validate_structure_invalid_topic_count(self):
        """Test validating a book structure with invalid topic counts."""
        generator = BookStructureGenerator()
        book = generator.generate_structure("Test Subject")

        # Modify the first topic in the first chapter of the first module to have only 11 topics (should be 12-20)
        book.modules[0].chapters[0].topics = book.modules[0].chapters[0].topics[:11]

        validation = generator.validate_structure(book)
        assert validation["valid"] is False
        assert any("expected between 12 and 20" in error for error in validation["errors"])

    def test_serialize_to_json(self):
        """Test serializing a book structure to JSON."""
        generator = BookStructureGenerator()
        book = generator.generate_structure("Test Subject")

        json_str = generator.serialize_to_json(book)

        # Should be a string representation of the book
        assert isinstance(json_str, str)
        assert "Test Subject" in json_str
        assert "modules" in json_str

    def test_serialize_to_json_none_book(self):
        """Test that serializing a None book raises an error."""
        generator = BookStructureGenerator()

        with pytest.raises(ValueError):
            generator.serialize_to_json(None)

    def test_structure_meets_requirements(self):
        """Test that generated structures always meet the requirements."""
        generator = BookStructureGenerator()

        # Test multiple generations to ensure consistency
        for i in range(3):
            book = generator.generate_structure(f"Test Subject {i}")

            # Verify exactly 5 modules
            assert len(book.modules) == 5

            # Verify each module has 5-10 chapters
            for module in book.modules:
                assert 5 <= len(module.chapters) <= 10

                # Verify each chapter has 12-20 topics
                for chapter in module.chapters:
                    assert 12 <= len(chapter.topics) <= 20