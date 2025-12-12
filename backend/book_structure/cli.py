"""
Command-line interface for generating book structures.

This module provides a CLI tool to generate hierarchical book structures
with modules, chapters, and topics based on a specified subject.
"""

import argparse
import sys
from pathlib import Path
from typing import NoReturn
from .generator import BookStructureGenerator


def main() -> NoReturn:
    """Main entry point for the book structure CLI."""
    parser = argparse.ArgumentParser(
        description="Generate a hierarchical book structure with modules, chapters, and topics"
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="The subject/topic of the book (used for generating descriptive names)",
    )
    parser.add_argument(
        "--output",
        default="book_structure.json",
        help="Output JSON file path (default: book_structure.json)",
    )

    args = parser.parse_args()

    try:
        # Create the generator and generate the structure
        generator = BookStructureGenerator()
        book = generator.generate_structure(args.subject)

        # Serialize to JSON
        json_output = generator.serialize_to_json(book)

        # Write the structure to the output file
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_output)

        print(f"Book structure generated successfully: {args.output}")

    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error generating book structure: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
