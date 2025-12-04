from fastapi import FastAPI
from pydantic import BaseModel
from rag.query import query_book

app = FastAPI(title="Book RAG Chatbot - Gemini")

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(req: ChatRequest):
    answer = query_book(req.question)
    return {"answer": answer}

@app.get("/")
def root():
    return {"status": "RAG chatbot running with Gemini API"}
