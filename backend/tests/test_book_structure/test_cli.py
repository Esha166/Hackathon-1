"""
Integration tests for the CLI module.

This module contains tests for the command-line interface functionality.
"""
import pytest
import subprocess
import sys
import json
import os
from pathlib import Path


class TestCLI:
    """Tests for the CLI functionality."""

    def test_cli_generation_success(self, tmp_path):
        """Test that CLI generates a valid book structure."""
        output_file = tmp_path / "test_output.json"
        subject = "Test Subject"

        # Run the CLI command
        cmd = [
            sys.executable,
            "-m",
            "backend.book_structure.cli",
            "--subject", subject,
            "--output", str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check that the command succeeded
        assert result.returncode == 0, f"CLI command failed with: {result.stderr}"

        # Check that the output file was created
        assert output_file.exists(), "Output file was not created"

        # Check that the output file contains valid JSON
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verify the structure
        assert "subject" in data
        assert data["subject"] == subject
        assert "modules" in data
        assert len(data["modules"]) == 5  # Should have exactly 5 modules

        # Verify each module has the right structure
        for module in data["modules"]:
            assert "name" in module
            assert "chapters" in module
            assert 5 <= len(module["chapters"]) <= 10  # 5-10 chapters per module

            # Verify each chapter
            for chapter in module["chapters"]:
                assert "name" in chapter
                assert "topics" in chapter
                assert 12 <= len(chapter["topics"]) <= 20  # 12-20 topics per chapter

    def test_cli_generation_with_different_subjects(self, tmp_path):
        """Test CLI with different subjects."""
        subjects = ["Mathematics", "Physics", "Biology"]

        for i, subject in enumerate(subjects):
            output_file = tmp_path / f"test_output_{i}.json"

            cmd = [
                sys.executable,
                "-m",
                "backend.book_structure.cli",
                "--subject", subject,
                "--output", str(output_file)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            assert result.returncode == 0, f"CLI command failed for subject {subject}: {result.stderr}"

            # Verify the subject in the output
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assert data["subject"] == subject

    def test_cli_generation_no_output_specified(self, tmp_path):
        """Test CLI when no output file is specified (should use default)."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)  # Change to temp directory to avoid polluting main dir

        try:
            # Run CLI without specifying output (should use default: book_structure.json)
            cmd = [
                sys.executable,
                "-m",
                "backend.book_structure.cli",
                "--subject", "Test Subject"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            assert result.returncode == 0, f"CLI command failed: {result.stderr}"

            # Check that the default output file was created
            default_file = tmp_path / "book_structure.json"
            assert default_file.exists(), "Default output file was not created"

            # Verify it's valid JSON with correct structure
            with open(default_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assert data["subject"] == "Test Subject"
            assert len(data["modules"]) == 5
        finally:
            os.chdir(original_cwd)  # Restore original directory

    def test_cli_generation_invalid_subject(self, tmp_path):
        """Test CLI with an empty subject (should fail)."""
        output_file = tmp_path / "test_output.json"

        cmd = [
            sys.executable,
            "-m",
            "backend.book_structure.cli",
            "--subject", "",  # Empty subject should cause validation error
            "--output", str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Command should fail due to validation error
        assert result.returncode != 0
        assert "Validation error" in result.stderr or "error" in result.stderr.lower()

    def test_cli_missing_subject_argument(self, tmp_path):
        """Test CLI when subject argument is missing (should fail)."""
        output_file = tmp_path / "test_output.json"

        cmd = [
            sys.executable,
            "-m",
            "backend.book_structure.cli",
            "--output", str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Command should fail due to missing required argument
        assert result.returncode != 0
        assert "error" in result.stderr.lower() or "usage" in result.stderr.lower()

    def test_cli_output_file_creation(self, tmp_path):
        """Test that CLI properly creates the output file with correct content."""
        output_file = tmp_path / "custom_output.json"
        subject = "Computer Science"

        cmd = [
            sys.executable,
            "-m",
            "backend.book_structure.cli",
            "--subject", subject,
            "--output", str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"CLI command failed: {result.stderr}"

        # Verify the file exists and has the right content
        assert output_file.exists()
        assert output_file.stat().st_size > 0  # File is not empty

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Should contain the subject and structure markers
        assert subject in content
        assert "modules" in content
        assert "chapters" in content
        assert "topics" in content

    def test_cli_large_structure_generation(self, tmp_path):
        """Test CLI generation with a complex subject to ensure it handles larger structures."""
        output_file = tmp_path / "large_structure.json"
        subject = "Advanced Quantum Computing and Machine Learning"

        cmd = [
            sys.executable,
            "-m",
            "backend.book_structure.cli",
            "--subject", subject,
            "--output", str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"CLI command failed: {result.stderr}"

        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verify the complete structure is generated correctly
        assert data["subject"] == subject
        assert len(data["modules"]) == 5

        total_chapters = 0
        total_topics = 0

        for module in data["modules"]:
            assert 5 <= len(module["chapters"]) <= 10
            total_chapters += len(module["chapters"])

            for chapter in module["chapters"]:
                assert 12 <= len(chapter["topics"]) <= 20
                total_topics += len(chapter["topics"])

        # Verify ranges are within expected bounds
        assert 25 <= total_chapters <= 50  # 5 modules * (5-10 chapters)
        assert 300 <= total_topics <= 1000  # total_chapters * (12-20 topics)