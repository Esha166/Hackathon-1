import os
import requests
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

client = QdrantClient(url=QDRANT_URL)

def get_embedding(text: str):
    url = "https://api.gemini.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {"model": "gemini-embeddings-small", "input": text}
    resp = requests.post(url, json=payload, headers=headers)
    return resp.json()["data"][0]["embedding"]

def get_gemini_answer(prompt: str):
    url = "https://api.gemini.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {
        "model": "gemini-4o",
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(url, json=payload, headers=headers)
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
