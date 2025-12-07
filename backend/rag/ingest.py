import os
import json # Keep json for potential future use or if parsing other formats
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

from .embedder import get_embedding # Import get_embedding from embedder.py
from .parser import process_docusaurus_content # Import the content parser

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
VECTOR_SIZE = 768 # Common embedding size for Gemini models

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set.")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def ingest_docusaurus_content(base_path: str):
    """
    Processes Docusaurus content, generates embeddings, and stores them in Qdrant collections.
    """
    all_content = process_docusaurus_content(base_path)

    collection_configs = {
        "book_text_chunks": {
            "metadata_keys": ["chapter_title", "section_heading", "page_number", "source_file", "text_chunk_id", "keywords"],
            "id_field": "text_chunk_id",
            "text_field": "content",
        },
        "code_snippets": {
            "metadata_keys": ["chapter_title", "section_heading", "language", "code_example_id", "keywords", "description", "source_file"],
            "id_field": "code_example_id",
            "text_field": "code",
        },
        "diagram_descriptions": {
            "metadata_keys": ["chapter_title", "section_heading", "figure_number", "description_id", "keywords", "alt_text", "url", "title", "source_file"],
            "id_field": "description_id",
            "text_field": "alt_text", # Or title, or combination
        },
    }

    for collection_name, config in collection_configs.items():
        print(f"Ingesting into collection: {collection_name}")
        points = []
        for item in all_content[collection_name]:
            text_to_embed = item[config["text_field"]]
            if not text_to_embed: # Skip if no text to embed
                continue

            vector = get_embedding(text_to_embed)
            
            payload = {key: item.get(key) for key in config["metadata_keys"]}
            payload["source_file"] = item.get("source_file") # Ensure source_file is always included

            # Ensure ID is a string
            point_id = str(item[config["id_field"]])

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            )
        
        # Ensure collection exists before upserting
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )

        if points:
            client.upsert(
                collection_name=collection_name,
                points=points,
                wait=True
            )
            print(f"Ingested {len(points)} items into {collection_name}")
        else:
            print(f"No items to ingest into {collection_name}")

if __name__ == "__main__":
    # Example usage: assuming current working directory is the project root
    project_root_path = os.getcwd()
    ingest_docusaurus_content(project_root_path)
