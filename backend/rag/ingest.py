import json
import os
import requests
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

client = QdrantClient(url=QDRANT_URL)

# Ensure collection exists
client.recreate_collection(collection_name="book_vectors", vector_size=1536)

def get_embedding(text: str):
    url = "https://api.gemini.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {"model": "gemini-embeddings-small", "input": text}
    resp = requests.post(url, json=payload, headers=headers)
    return resp.json()["data"][0]["embedding"]

def ingest_book(book_json_path: str):
    with open(book_json_path, "r", encoding="utf-8") as f:
        book = json.load(f)

    points = []
    for module, chapters in book.items():
        for chapter, topics in chapters.items():
            text = "\n".join(topics)
            embedding = get_embedding(text)
            points.append({
                "id": f"{module}-{chapter}",
                "vector": embedding,
                "payload": {"module": module, "chapter": chapter, "topics": topics, "text": text}
            })

    client.upsert(collection_name="book_vectors", points=points)
    print(f"Ingested {len(points)} chapters into Qdrant")
