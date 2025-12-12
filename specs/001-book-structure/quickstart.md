# Quickstart: Book Structure Generation

## Overview
This guide explains how to use the book structure generation feature to create hierarchical book structures with modules, chapters, and topics. The feature generates exactly 5 modules with descriptive names, each containing 5-10 chapters with descriptive names, and each chapter containing 12-20 topics with realistic names based on potential subject matter.

## Prerequisites
- Python 3.11+
- FastAPI backend running

## Usage

### 1. Import the Generator
```python
from backend.book_structure.generator import generate_book_structure
```

### 2. Call the Generation Function
```python
# Generate a book structure with default parameters
book_structure = generate_book_structure()

# Or specify custom ranges (though the spec requires fixed values)
book_structure = generate_book_structure(
    num_modules=5,
    min_chapters_per_module=5,
    max_chapters_per_module=10,
    min_topics_per_chapter=12,
    max_topics_per_chapter=20
)
```

### 3. Access the Generated Structure
```python
# The result is a Python dict that can be serialized to JSON
import json
json_output = json.dumps(book_structure, indent=2)
print(json_output)
```

### 4. Error Handling
```python
# The function will return detailed error messages for validation failures
try:
    book_structure = generate_book_structure()
except ValueError as e:
    print(f"Validation error: {e}")
```

## API Integration
The function can be integrated into a FastAPI endpoint with detailed error reporting:

```python
from fastapi import FastAPI
from backend.book_structure.generator import generate_book_structure

app = FastAPI()

@app.get("/book-structure")
def get_book_structure():
    try:
        return generate_book_structure()
    except ValueError as e:
        # Return detailed error messages as specified in clarifications
        return {"error": str(e)}
```

## Testing
Run the tests to verify the functionality:
```bash
pytest backend/tests/test_book_structure/
```