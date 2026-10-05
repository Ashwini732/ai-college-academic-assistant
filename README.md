# AI-Based College Academic Assistant

An AI-powered college assistant using LLM, RAG, LangChain, LangGraph, FastAPI and React.

## Features

- Academic Q&A using college documents
- Document summarization
- Calculator
- Academic deadline calculation
- Personalized study plan generation
- Study plan modification
- Handles unavailable information

## Tech Stack

- Python
- LangChain
- LangGraph
- ChromaDB
- FastAPI
- React + Vite
- OpenRouter LLM
- HuggingFace Embeddings

## Project Structure

ai-college-academic-assistant/
├── api/
│   └── main.py
├── data/
├── src/
│   ├── chains.py
│   ├── graph.py
│   ├── planner.py
│   ├── rag.py
│   └── tools.py
├── frontend/
├── requirements.txt
├── .env
└── README.md

## Setup

### 1. Clone the repository

git clone <REPOSITORY_URL>
cd ai-college-academic-assistant

### 2. Create virtual environment

python -m venv .venv

.venv\Scripts\Activate.ps1

### 3. Install Python dependencies

pip install -r requirements.txt

### 4. Create .env

Create a `.env` file in the project root:

OPENROUTER_API_KEY=your_api_key

### 5. Run Backend

From the project root:

uvicorn api.main:app --reload

Backend:
http://127.0.0.1:8000

API Documentation:
http://127.0.0.1:8000/docs

### 6. Run Frontend

Open a second terminal:

cd frontend
npm install
npm run dev

Frontend:
http://localhost:5173

## Example Queries

What is the minimum attendance requirement?

Summarize the internship guidelines

What is 25 * 4 + 10?

How many days are left for semester exams?

Make a study plan for Algorithms and Databases,
3 hours a day, exam on 2026-11-20

Give more time to Algorithms

## Important

Do not commit `.env` or `.venv`.

Each team member must create their own `.env` file with their API key.
