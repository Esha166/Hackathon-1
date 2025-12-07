from typing import List
import os
import requests
from dotenv import load_dotenv

load_dotenv() # Ensure environment variables are loaded
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiEmbedder:
    def __init__(self, api_key: str = GEMINI_API_KEY):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for embedding.")
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.embedding_url = "https://api.gemini.com/v1/embeddings"
        self.embedding_model = "gemini-embeddings-small" # As per query.py and ingest.py

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        Generates vector embeddings for a list of texts using the Gemini API.
        """
        if not texts:
            return []

        # The Gemini embeddings API typically takes a single string or a list of strings
        # For this simplified version, we'll assume it takes a list.
        # If the API only takes single strings, this would need a loop.
        
        payload = {"model": self.embedding_model, "input": texts if len(texts) > 1 else texts[0]}
        
        try:
            resp = requests.post(self.embedding_url, json=payload, headers=self.headers)
            resp.raise_for_status() # Raise an exception for HTTP errors
            
            response_json = resp.json()
            if "data" in response_json and len(response_json["data"]) > 0 and "embedding" in response_json["data"][0]:
                if len(texts) > 1: # Assuming API returns list of embeddings for list of texts
                    return [item["embedding"] for item in response_json["data"]]
                else: # Assuming API returns single embedding for single text
                    return [response_json["data"][0]["embedding"]]
            else:
                raise ValueError(f"Invalid response from embedding API: {response_json}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling Gemini embedding API: {e}")

# Global instance for convenience
gemini_embedder = GeminiEmbedder()

def get_embedding(text: str) -> List[float]:
    """
    Convenience function to get a single embedding.
    """
    return gemini_embedder.embed_text([text])[0]

# Example Usage (for testing the embedder directly)
if __name__ == "__main__":
    try:
        sample_texts_single = "This is a sample text about AI."
        embedding_single = get_embedding(sample_texts_single)
        print(f"\nGenerated single embedding. Snippet: {embedding_single[:5]}...")

        sample_texts_multiple = [
            "Humanoid robotics are fascinating.",
            "Another piece of content to embed."
        ]
        embeddings_multiple = gemini_embedder.embed_text(sample_texts_multiple)
        print(f"\nGenerated multiple embeddings. First snippet: {embeddings_multiple[0][:5]}...")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure GEMINI_API_KEY is set in your .env file and is valid.")
    except RuntimeError as e:
        print(f"Runtime Error: {e}")