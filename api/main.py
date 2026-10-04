import sys
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from graph import ask

app = FastAPI(title="AI College Academic Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    text: str


class Question(BaseModel):
    question: str
    history: List[Message] = []


@app.get("/")
def root():
    return {"message": "AI College Academic Assistant API is running"}


@app.post("/ask")
def ask_question(data: Question):
    history = [{"role": item.role, "text": item.text} for item in data.history]
    answer = ask(data.question, history)

    return {
        "question": data.question,
        "answer": answer
    }