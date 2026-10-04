from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.graph import ask

app = FastAPI(title="AI College Academic Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "AI College Academic Assistant API is running"}


@app.post("/ask")
def ask_question(data: Question):
    answer = ask(data.question)

    return {
        "question": data.question,
        "answer": answer
    }