import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load environment variables (.env)
load_dotenv()

# 2. Paths
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
VECTOR_DB_FOLDER = PROJECT_FOLDER / "vector_db"

# 3. Load Embedding Model
print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# 4. Load existing Chroma Vector DB
print("Connecting to existing Chroma vector database...")
vector_store = Chroma(
    persist_directory=str(VECTOR_DB_FOLDER),
    embedding_function=embeddings,
    collection_name="college_documents"
)

# 5. Create Retriever (Top 3 relevant chunks)
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 6. Initialize LLM via OpenRouter + ChatOpenAI
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file!")

llm = ChatOpenAI(
    model_name="openai/gpt-4o-mini",
    openai_api_key=openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0
)

# 7. Define Prompt Template (Strictly Grounded to avoid hallucinations)
prompt_template = ChatPromptTemplate.from_template(
    """You are an AI-based College Academic Assistant. 

Answer the question strictly using only the provided context from the college documents. 
If the information is not present in the context, clearly state: "The information was not found in the uploaded college documents." Do not try to make up or infer answers.

Context:
{context}

Question:
{question}

Answer:"""
)

# Helper function to format context chunks for the prompt
def format_docs(docs):
    return "\n\n".join(f"--- Chunk ---\n{doc.page_content}" for doc in docs)


# 8. RAG Execution Function
def query_rag(question: str):
    print(f"\n==========================================")
    print(f"User Question: {question}")
    print(f"==========================================")

    # Step A: Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        print("No documents retrieved.")
        return

    # Step B: Format retrieved context
    context_text = format_docs(retrieved_docs)

    # Step C: Format Prompt and invoke LLM
    chain = prompt_template | llm | StrOutputParser()
    answer = chain.invoke({"context": context_text, "question": question})

    # Step D: Print Answer
    print("\n[AI ANSWER]")
    print(answer)

    # Step E: Print Retrieved Context Sources & Page Numbers
    print("\n[SOURCES & METADATA]")
    for idx, doc in enumerate(retrieved_docs, 1):
        source_file = doc.metadata.get("source_file", doc.metadata.get("source", "Unknown"))
        page_num = doc.metadata.get("page", "Unknown")
        
        # If PyPDFLoader used 0-indexed page numbers, convert to 1-indexed for display
        if isinstance(page_num, int):
            page_num += 1

        print(f"  Chunk {idx}:")
        print(f"    - File: {source_file}")
        print(f"    - Page: {page_num}")


# 9. Test Pipeline
if __name__ == "__main__":
    test_questions = [
        "What is the minimum attendance requirement?",
        "What are the rules for Additional Mathematics?",
        "What are the internship requirements?",
        "What is the policy for space travel?"  # Test for unknown handling
    ]

    for q in test_questions:
        query_rag(q)