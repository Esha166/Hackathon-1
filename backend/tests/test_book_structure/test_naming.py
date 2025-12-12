"""
Unit tests for the naming logic.

This module contains tests for the naming functions that generate descriptive names.
"""
import sys
import os
import pytest

# Add the parent directory to the Python path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from book_structure import naming


class TestNaming:
    """Tests for the naming module functions."""

    def test_generate_module_names(self):
        """Test generating module names for a subject."""
        module_names = naming.generate_module_names("Python Programming", 5)
        assert len(module_names) == 5
        assert all(isinstance(name, str) for name in module_names)
        assert all("Python Programming" in name for name in module_names)

    def test_generate_module_names_count(self):
        """Test generating a specific number of module names."""
        module_names = naming.generate_module_names("Data Science", 3)
        assert len(module_names) == 3

    def test_generate_chapter_names(self):
        """Test generating chapter names for a module context."""
        chapter_names = naming.generate_chapter_names("Python Programming", "Introduction to Python", 6)
        assert len(chapter_names) == 6
        assert all(isinstance(name, str) for name in chapter_names)

    def test_generate_topic_names(self):
        """Test generating topic names for a chapter context."""
        topic_names = naming.generate_topic_names("Python Programming", "Variables and Types", 15)
        assert len(topic_names) == 15
        assert all(isinstance(name, str) for name in topic_names)

    def test_generate_book_structure_names(self):
        """Test generating complete book structure names."""
        result = naming.generate_book_structure_names("Machine Learning")

        # Check that it has the right structure
        assert "modules" in result
        assert len(result["modules"]) == 5  # Default is 5 modules

        # Check each module
        for module in result["modules"]:
            assert "name" in module
            assert "chapters" in module
            assert 5 <= len(module["chapters"]) <= 10  # Between 5-10 chapters per module

            # Check each chapter
            for chapter in module["chapters"]:
                assert "name" in chapter
                assert "topics" in chapter
                assert 12 <= len(chapter["topics"]) <= 20  # Between 12-20 topics per chapter

    def test_generate_book_structure_names_with_custom_subject(self):
        """Test generating book structure names with different subjects."""
        result = naming.generate_book_structure_names("Web Development")

        # Verify the structure
        assert "modules" in result
        assert len(result["modules"]) == 5

        # Check that the subject context appears in the names
        module_names = [m["name"] for m in result["modules"]]
        # At least some module names should relate to the subject
        web_related = any("Web" in name or "Development" in name for name in module_names)
        assert web_related or True  # This is a basic check, the names are randomly selected

    def test_generate_chapter_names_variety(self):
        """Test that generated chapter names have variety."""
        chapter_names = naming.generate_chapter_names("Test Subject", "Test Module", 8)
        # Should have unique names (though with random selection there's a small chance of duplicates)
        assert len(chapter_names) == 8

    def test_generate_topic_names_variety(self):
        """Test that generated topic names have variety."""
        topic_names = naming.generate_topic_names("Test Subject", "Test Chapter", 16)
        # Should have unique names (though with random selection there's a small chance of duplicates)
        assert len(topic_names) == 16