import os
import requests
from qdrant_client import QdrantClient
from dotenv import load_dotenv

from .embedder import get_embedding # Import get_embedding from embedder.py

load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # No longer needed here as embedder handles it
QDRANT_URL = os.getenv("QDRANT_URL")

client = QdrantClient(url=QDRANT_URL)

# Removed local get_embedding definition

def get_gemini_answer(prompt: str):
    url = "https://api.gemini.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('GEMINI_API_KEY')}"} # Use os.getenv directly here
    payload = {
        "model": "gemini-4o",
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status() # Raise an exception for HTTP errors
    return resp.json()["choices"][0]["message"]["content"]

def query_book(question: str, top_k: int = 3) -> str:
    # Question embedding
    query_vector = get_embedding(question)

    # Search Qdrant
    search_result = client.search(
        collection_name="book_vectors",
        query_vector=query_vector,
        limit=top_k
    )

    # Combine top-k text for LLM context
    context = "\n".join([hit.payload["text"] for hit in search_result])
    prompt = f"Answer the question based ONLY on the following context:\n{context}\n\nQuestion: {question}"

    answer = get_gemini_answer(prompt)
    return answer