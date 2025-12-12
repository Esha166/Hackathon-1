"""
Unit tests for the book structure models.

This module contains tests for the Pydantic models: Topic, Chapter, Module, and Book.
"""
import sys
import os
import pytest

# Add the parent directory to the Python path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from book_structure.models import Topic, Chapter, Module, Book


class TestTopic:
    """Tests for the Topic model."""

    def test_topic_creation_valid(self):
        """Test creating a Topic with valid data."""
        topic = Topic(name="Introduction to Python")
        assert topic.name == "Introduction to Python"
        assert topic.description is None

    def test_topic_creation_with_description(self):
        """Test creating a Topic with a description."""
        topic = Topic(name="Introduction to Python", description="A basic overview")
        assert topic.name == "Introduction to Python"
        assert topic.description == "A basic overview"

    def test_topic_name_empty(self):
        """Test that creating a Topic with an empty name raises an error."""
        with pytest.raises(ValueError):
            Topic(name="")

    def test_topic_name_whitespace_only(self):
        """Test that creating a Topic with only whitespace raises an error."""
        with pytest.raises(ValueError):
            Topic(name="   ")


class TestChapter:
    """Tests for the Chapter model."""

    def test_chapter_creation_valid(self):
        """Test creating a Chapter with valid data."""
        topics = [Topic(name=f"Topic {i}") for i in range(15)]
        chapter = Chapter(name="Variables and Types", topics=topics)
        assert chapter.name == "Variables and Types"
        assert len(chapter.topics) == 15

    def test_chapter_min_topics(self):
        """Test that a Chapter must have at least 12 topics."""
        topics = [Topic(name=f"Topic {i}") for i in range(12)]
        chapter = Chapter(name="Variables and Types", topics=topics)
        assert len(chapter.topics) == 12

    def test_chapter_max_topics(self):
        """Test that a Chapter must have at most 20 topics."""
        topics = [Topic(name=f"Topic {i}") for i in range(20)]
        chapter = Chapter(name="Variables and Types", topics=topics)
        assert len(chapter.topics) == 20

    def test_chapter_too_few_topics(self):
        """Test that creating a Chapter with fewer than 12 topics raises an error."""
        topics = [Topic(name=f"Topic {i}") for i in range(11)]
        with pytest.raises(ValueError):
            Chapter(name="Variables and Types", topics=topics)

    def test_chapter_too_many_topics(self):
        """Test that creating a Chapter with more than 20 topics raises an error."""
        topics = [Topic(name=f"Topic {i}") for i in range(21)]
        with pytest.raises(ValueError):
            Chapter(name="Variables and Types", topics=topics)

    def test_chapter_name_empty(self):
        """Test that creating a Chapter with an empty name raises an error."""
        topics = [Topic(name=f"Topic {i}") for i in range(15)]
        with pytest.raises(ValueError):
            Chapter(name="", topics=topics)

    def test_chapter_duplicate_topic_names(self):
        """Test that creating a Chapter with duplicate topic names raises an error."""
        topics = [Topic(name="Duplicate Topic") for i in range(15)]
        with pytest.raises(ValueError):
            Chapter(name="Variables and Types", topics=topics)


class TestModule:
    """Tests for the Module model."""

    def test_module_creation_valid(self):
        """Test creating a Module with valid data."""
        chapters = []
        for i in range(7):
            topics = [Topic(name=f"Topic {j}") for j in range(15)]
            chapter = Chapter(name=f"Chapter {i}", topics=topics)
            chapters.append(chapter)

        module = Module(name="Basic Concepts", chapters=chapters)
        assert module.name == "Basic Concepts"
        assert len(module.chapters) == 7

    def test_module_min_chapters(self):
        """Test that a Module must have at least 5 chapters."""
        chapters = []
        for i in range(5):
            topics = [Topic(name=f"Topic {j}") for j in range(15)]
            chapter = Chapter(name=f"Chapter {i}", topics=topics)
            chapters.append(chapter)

        module = Module(name="Basic Concepts", chapters=chapters)
        assert len(module.chapters) == 5

    def test_module_max_chapters(self):
        """Test that a Module must have at most 10 chapters."""
        chapters = []
        for i in range(10):
            topics = [Topic(name=f"Topic {j}") for j in range(15)]
            chapter = Chapter(name=f"Chapter {i}", topics=topics)
            chapters.append(chapter)

        module = Module(name="Basic Concepts", chapters=chapters)
        assert len(module.chapters) == 10

    def test_module_too_few_chapters(self):
        """Test that creating a Module with fewer than 5 chapters raises an error."""
        chapters = []
        for i in range(4):
            topics = [Topic(name=f"Topic {j}") for j in range(15)]
            chapter = Chapter(name=f"Chapter {i}", topics=topics)
            chapters.append(chapter)

        with pytest.raises(ValueError):
            Module(name="Basic Concepts", chapters=chapters)

    def test_module_too_many_chapters(self):
        """Test that creating a Module with more than 10 chapters raises an error."""
        chapters = []
        for i in range(11):
            topics = [Topic(name=f"Topic {j}") for j in range(15)]
            chapter = Chapter(name=f"Chapter {i}", topics=topics)
            chapters.append(chapter)

        with pytest.raises(ValueError):
            Module(name="Basic Concepts", chapters=chapters)

    def test_module_name_empty(self):
        """Test that creating a Module with an empty name raises an error."""
        chapters = []
        for i in range(7):
            topics = [Topic(name=f"Topic {j}") for j in range(15)]
            chapter = Chapter(name=f"Chapter {i}", topics=topics)
            chapters.append(chapter)

        with pytest.raises(ValueError):
            Module(name="", chapters=chapters)


class TestBook:
    """Tests for the Book model."""

    def test_book_creation_valid(self):
        """Test creating a Book with valid data."""
        modules = []
        for i in range(5):
            chapters = []
            for j in range(7):
                topics = [Topic(name=f"Topic {k}") for k in range(15)]
                chapter = Chapter(name=f"Chapter {j}", topics=topics)
                chapters.append(chapter)
            module = Module(name=f"Module {i}", chapters=chapters)
            modules.append(module)

        book = Book(subject="Python Programming", modules=modules)
        assert book.subject == "Python Programming"
        assert len(book.modules) == 5

    def test_book_exactly_5_modules(self):
        """Test that a Book must have exactly 5 modules."""
        modules = []
        for i in range(5):
            chapters = []
            for j in range(7):
                topics = [Topic(name=f"Topic {k}") for k in range(15)]
                chapter = Chapter(name=f"Chapter {j}", topics=topics)
                chapters.append(chapter)
            module = Module(name=f"Module {i}", chapters=chapters)
            modules.append(module)

        book = Book(subject="Python Programming", modules=modules)
        assert len(book.modules) == 5

    def test_book_wrong_number_of_modules(self):
        """Test that creating a Book with other than 5 modules raises an error."""
        modules = []
        for i in range(4):  # Only 4 modules instead of 5
            chapters = []
            for j in range(7):
                topics = [Topic(name=f"Topic {k}") for k in range(15)]
                chapter = Chapter(name=f"Chapter {j}", topics=topics)
                chapters.append(chapter)
            module = Module(name=f"Module {i}", chapters=chapters)
            modules.append(module)

        with pytest.raises(ValueError):
            Book(subject="Python Programming", modules=modules)

        # Test with 6 modules
        modules = []
        for i in range(6):  # 6 modules instead of 5
            chapters = []
            for j in range(7):
                topics = [Topic(name=f"Topic {k}") for k in range(15)]
                chapter = Chapter(name=f"Chapter {j}", topics=topics)
                chapters.append(chapter)
            module = Module(name=f"Module {i}", chapters=chapters)
            modules.append(module)

        with pytest.raises(ValueError):
            Book(subject="Python Programming", modules=modules)