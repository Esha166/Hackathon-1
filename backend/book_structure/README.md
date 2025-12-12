# Book Structure Generator

A Python module for generating hierarchical book structures with descriptive names based on a subject. The generator creates exactly 5 modules, each containing 5-10 chapters, and each chapter containing 12-20 topics.

## Installation

The module is part of the backend package and uses standard Python dependencies. To install the required dependencies:

```bash
pip install -r backend/requirements.txt
```

Or install the specific dependencies directly:

```bash
pip install pydantic
```

## Usage

### Command Line Interface

The module provides a command-line interface for generating book structures:

```bash
python -m backend.book_structure.cli --subject "Your Subject" --output output_file.json
```

#### Options:
- `--subject` (required): The subject or topic of the book
- `--output` (optional): Output JSON file path (default: book_structure.json)

#### Examples:
```bash
# Generate a book structure with default output file
python -m backend.book_structure.cli --subject "Python Programming"

# Generate a book structure with custom output file
python -m backend.book_structure.cli --subject "Machine Learning" --output ml_book.json

# Generate a book structure with a complex subject
python -m backend.book_structure.cli --subject "Advanced Quantum Computing" --output quantum_book.json
```

### Python API

You can also use the module programmatically:

```python
from backend.book_structure.generator import BookStructureGenerator

# Create a generator instance
generator = BookStructureGenerator()

# Generate a book structure
book = generator.generate_structure("Python Programming")

# Serialize to JSON
json_output = generator.serialize_to_json(book)

# Or validate the structure
validation = generator.validate_structure(book)
print(f"Valid: {validation['valid']}")
print(f"Errors: {validation['errors']}")
```

## JSON Output Format

The generated JSON follows this structure:

```json
{
  "subject": "string",
  "modules": [
    {
      "name": "string",
      "chapters": [
        {
          "name": "string",
          "topics": [
            {
              "name": "string",
              "description": "string (optional)"
            }
          ]
        }
      ]
    }
  ]
}
```

### Format Specifications:
- `subject`: The main subject of the book (string)
- `modules`: Array of exactly 5 modules
  - Each module has:
    - `name`: Descriptive name based on the subject (string)
    - `chapters`: Array of 5-10 chapters per module
      - Each chapter has:
        - `name`: Descriptive name based on module context (string)
        - `topics`: Array of 12-20 topics per chapter
          - Each topic has:
            - `name`: Descriptive name based on chapter context (string)
            - `description`: Optional description (string)

### Example Output Structure:
```json
{
  "subject": "Python Programming",
  "modules": [
    {
      "name": "Python Programming: Introduction to Python",
      "chapters": [
        {
          "name": "Python Programming: Getting Started with Python",
          "topics": [
            {
              "name": "Python Programming: Understanding Python Syntax"
            },
            {
              "name": "Python Programming: Installing Python Environment"
            }
          ]
        }
      ]
    }
  ]
}
```

## Validation

The generator includes built-in validation that ensures:
- Exactly 5 modules are created
- Each module contains 5-10 chapters
- Each chapter contains 12-20 topics
- All names are descriptive and contextually relevant
- No empty or whitespace-only names

## Architecture

The module consists of several components:

- `models.py`: Pydantic models for Topic, Chapter, Module, and Book with validation
- `naming.py`: Functions for generating descriptive names based on context
- `generator.py`: BookStructureGenerator class with generation and validation logic
- `cli.py`: Command-line interface implementation

## Testing

To run the tests for this module:

```bash
pytest backend/tests/test_book_structure/
```

The test suite includes:
- Unit tests for models validation
- Unit tests for naming logic
- Unit tests for generator functionality
- Integration tests for CLI