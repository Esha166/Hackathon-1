from typing import List, Dict, Any
import os
import re
import frontmatter

def parse_markdown_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses a Markdown file to extract text chunks and metadata.
    Each chunk will have a source_file, chapter_title, section_heading,
    page_number (sequential), text_chunk_id, and keywords.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    post = frontmatter.loads(content)
    text_content = post.content
    metadata = post.metadata

    chunks = []
    
    # Determine chapter title from frontmatter or filename
    chapter_title = metadata.get('title', os.path.basename(file_path).replace('.md', '').replace('.mdx', ''))
    
    # Split content by headings to identify sections and chunks
    # This regex splits by any heading (H1-H6)
    split_content = re.split(r'(^#+\s.*)', text_content, flags=re.MULTILINE)

    current_section_heading = ""
    chunk_counter = 0

    # The first element before any heading is also content
    if split_content[0].strip():
        chunks.append({
            "content": split_content[0].strip(),
            "source_file": file_path,
            "chapter_title": chapter_title,
            "section_heading": "Introduction", # Default for initial text
            "page_number": chunk_counter + 1,
            "text_chunk_id": f"{os.path.basename(file_path)}_chunk{chunk_counter}",
            "keywords": [],
        })
        chunk_counter += 1

    for i in range(1, len(split_content), 2):
        heading = split_content[i].strip()
        text = split_content[i+1].strip() if (i+1) < len(split_content) else ""

        # Update current section heading based on the heading
        current_section_heading = heading.lstrip('# ').strip()
        
        if text:
            chunks.append({
                "content": text,
                "source_file": file_path,
                "chapter_title": chapter_title,
                "section_heading": current_section_heading,
                "page_number": chunk_counter + 1,
                "text_chunk_id": f"{os.path.basename(file_path)}_chunk{chunk_counter}",
                "keywords": [],
            })
            chunk_counter += 1
            
    return chunks

def extract_code_snippets(content: str, file_path: str, chapter_title: str, section_heading: str) -> List[Dict[str, Any]]:
    """
    Extracts code snippets from Markdown content.
    Adds source_file, chapter_title, section_heading metadata.
    """
    snippets = []
    code_block_regex = re.compile(r'```(?P<lang>\w+)?\n(?P<code>.*?)`' + '``', re.DOTALL)
    for i, match in enumerate(code_block_regex.finditer(content)):
        lang = match.group('lang') if match.group('lang') else 'plaintext'
        code = match.group('code').strip()
        if code:
            snippets.append({
                "code": code,
                "language": lang,
                "code_example_id": f"{os.path.basename(file_path)}_code{i}",
                "description": "", 
                "keywords": [],
                "source_file": file_path,
                "chapter_title": chapter_title,
                "section_heading": section_heading,
            })
    return snippets

def extract_diagram_descriptions(content: str, file_path: str, chapter_title: str, section_heading: str) -> List[Dict[str, Any]]:
    """
    Extracts diagram descriptions (e.g., alt text from images) from Markdown content.
    Adds source_file, chapter_title, section_heading metadata.
    """
    descriptions = []
    image_regex = re.compile(r'!\[''(?P<alt_text>.*?)''\]\((?P<url>.*?)(?:\s"(?P<title>.*?)?")?\)')
    for i, match in enumerate(image_regex.finditer(content)):
        alt_text = match.group('alt_text').strip()
        url = match.group('url').strip()
        title = match.group('title').strip() if match.group('title') else alt_text

        if alt_text or title:
            descriptions.append({
                "alt_text": alt_text,
                "url": url,
                "title": title,
                "description_id": f"{os.path.basename(file_path)}_diagram{i}",
                "keywords": [],
                "source_file": file_path,
                "chapter_title": chapter_title,
                "section_heading": section_heading,
                "figure_number": i + 1,
            })
    return descriptions

def process_docusaurus_content(base_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Processes all Markdown files in Docusaurus content directories (docs and blog)
    and extracts text chunks, code snippets, and diagram descriptions.
    """
    all_content: Dict[str, List[Dict[str, Any]]] = {
        "book_text_chunks": [],
        "code_snippets": [],
        "diagram_descriptions": [],
    }

    content_dirs = [
        os.path.join(base_path, 'frontend', 'website', 'docs'),
        os.path.join(base_path, 'frontend', 'website', 'blog'),
    ]

    for content_dir in content_dirs:
        for root, _, files in os.walk(content_dir):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)
                    print(f"Processing {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        full_content = f.read()
                    
                    post = frontmatter.loads(full_content)
                    text_content_only = post.content # Content without frontmatter
                    chapter_title = post.metadata.get('title', os.path.basename(file_path).replace('.md', '').replace('.mdx', ''))

                    # Extract text chunks
                    all_content["book_text_chunks"].extend(parse_markdown_file(file_path))

                    # Process content in sections for code and diagrams
                    split_content_by_headings = re.split(r'(^#+\s.*)', text_content_only, flags=re.MULTILINE)
                    
                    current_section_heading = "Introduction" # Default for content before first heading
                    
                    # Handle content before the first heading
                    if split_content_by_headings[0].strip():
                        # Extract code and diagrams from initial text
                        all_content["code_snippets"].extend(extract_code_snippets(split_content_by_headings[0], file_path, chapter_title, current_section_heading))
                        all_content["diagram_descriptions"].extend(extract_diagram_descriptions(split_content_by_headings[0], file_path, chapter_title, current_section_heading))


                    for i in range(1, len(split_content_by_headings), 2):
                        heading = split_content_by_headings[i].strip()
                        text_in_section = split_content_by_headings[i+1].strip() if (i+1) < len(split_content_by_headings) else ""

                        current_section_heading = heading.lstrip('# ').strip()
                        
                        if text_in_section:
                            all_content["code_snippets"].extend(extract_code_snippets(text_in_section, file_path, chapter_title, current_section_heading))
                            all_content["diagram_descriptions"].extend(extract_diagram_descriptions(text_in_section, file_path, chapter_title, current_section_heading))
    
    return all_content

if __name__ == "__main__":
    # Example Usage (for testing the parser directly)
    sample_markdown = """
---
title: Introduction to AI
authors: [John Doe]
date: 2025-12-07
---
# Chapter 1: What is AI?

This is an **introduction** to Artificial Intelligence.

## History of AI
AI has a rich history, starting from early philosophical inquiries.

```python
def hello_ai():
    print("Hello, AI!")
```

## AI Applications
AI is used in many fields.

![Flowchart of AI process](img/ai_flow.png "AI Process Overview")

### Machine Learning
A subfield of AI.

```javascript
// A JS example
console.log("ML in JS");
```
    """
    
    # Save sample markdown to a temporary file
    temp_file = "temp_sample.md"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(sample_markdown)

    print(f"--- Parsing {temp_file} ---")
    text_chunks = parse_markdown_file(temp_file)
    print("\nText Chunks:")
    for chunk in text_chunks:
        print(f"- Chapter: {chunk['chapter_title']}, Section: {chunk['section_heading']}, Page: {chunk['page_number']}")
        print(f"  Content: {chunk['content'][:50]}...")
        
    code_snippets = extract_code_snippets(sample_markdown, temp_file, "Test Chapter", "General")
    print("\nCode Snippets:")
    for snippet in code_snippets:
        print(f"- Language: {snippet['language']}, Code: {snippet['code'][:50]}...")

    diagram_descriptions = extract_diagram_descriptions(sample_markdown, temp_file, "Test Chapter", "General")
    print("\nDiagram Descriptions:")
    for desc in diagram_descriptions:
        print(f"- Alt Text: {desc['alt_text']}, URL: {desc['url']}")

    os.remove(temp_file)

    print("\n--- Processing all Docusaurus content ---")
    # Assuming current working directory is the project root
    project_root_path = os.getcwd() 
    all_extracted_content = process_docusaurus_content(project_root_path)

    print(f"\nTotal Text Chunks: {len(all_extracted_content['book_text_chunks'])}")
    print(f"Total Code Snippets: {len(all_extracted_content['code_snippets'])}")
    print(f"Total Diagram Descriptions: {len(all_extracted_content['diagram_descriptions'])}")

    # Example of first few extracted items
    if all_extracted_content['book_text_chunks']:
        print("\nFirst Text Chunk Example:")
        print(all_extracted_content['book_text_chunks'][0])
    if all_extracted_content['code_snippets']:
        print("\nFirst Code Snippet Example:")
        print(all_extracted_content['code_snippets'][0])
    if all_extracted_content['diagram_descriptions']:
        print("\nFirst Diagram Description Example:")
        print(all_extracted_content['diagram_descriptions'][0])