import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load environment variables
load_dotenv()

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
VECTOR_DB_FOLDER = PROJECT_FOLDER / "vector_db"

# 2. Load Embedding Model
print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# 3. Load Chroma Vector DB
print("Connecting to Chroma vector database...")
vector_store = Chroma(
    persist_directory=str(VECTOR_DB_FOLDER),
    embedding_function=embeddings,
    collection_name="college_documents"
)

# 4. Create Retriever (k=6 ensures coverage for both PDF & Web sources)
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 6}
)

# 5. LLM Setup via OpenRouter
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file!")

llm = ChatOpenAI(
    model_name="openai/gpt-4o-mini",
    openai_api_key=openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0
)

# 6. User-Facing Prompt Template
prompt_template = ChatPromptTemplate.from_template(
    """You are an AI-based College Academic Assistant.

Answer the user's question directly, clearly, and concisely using ONLY the provided context below. 

Guidelines:
1. Provide a well-structured, easy-to-read answer using bullet points or numbered lists where appropriate.
2. Do not mention document file names, page numbers, chunk numbers, or internal technical details.
3. If the requested information is not in the context, respond with: "I'm sorry, but that information is not available in the uploaded college documents or website."
4. Do not make up or infer information beyond what is directly stated.

Context:
{context}

Question:
{question}

Answer:"""
)

def format_docs(docs):
    seen_text = set()
    unique_chunks = []
    for doc in docs:
        content = doc.page_content.strip()
        if content not in seen_text:
            seen_text.add(content)
            unique_chunks.append(content)
    return "\n\n".join(unique_chunks)

def query_rag(question: str):
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        print("I'm sorry, but no relevant information was found.")
        return

    context_text = format_docs(retrieved_docs)

    chain = prompt_template | llm | StrOutputParser()
    answer = chain.invoke({"context": context_text, "question": question})

    print(f"\nUser Question: {question}")
    print("-" * 60)
    print(answer)
    print("=" * 60)

if __name__ == "__main__":
    # Comprehensive Test Suite
    test_questions = [
        # --- Academic & Attendance Rules (PDF Focus) ---
        "What is the minimum attendance requirement?",
        "What are the rules for Additional Mathematics?",
        "What happens if a student gets an F grade in a course?",
        "What are the rules regarding Continuous Internal Evaluation (CIE)?",

        # --- Degree & Credit System (PDF Focus) ---
        "How many total credits are required for the award of the B.Tech degree?",
        "What are the criteria for promotion to higher semesters?",

        # --- Placement & Career Information (Website Focus) ---
        "What companies visit for placements?",
        "What are the highest and average salary packages offered during placements?",
        "Which major recruiters offer placement opportunities for engineering students?",

        # --- Edge Cases & Guardrail Check ---
        "What is the policy for hostel fee refunds?",
        "Can students apply for campus space missions?"
    ]

    for q in test_questions:
        query_rag(q)