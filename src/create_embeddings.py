from pathlib import Path

from split_documents import chunks
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# -----------------------------
# 1. Paths
# -----------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
VECTOR_DB_FOLDER = PROJECT_FOLDER / "vector_db"


# -----------------------------
# 2. Documents
# -----------------------------

print("\nTotal chunks received:", len(chunks))


# -----------------------------
# 3. Create embeddings
# -----------------------------

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

print("Embedding model loaded.")


# -----------------------------
# 4. Create Chroma database
# -----------------------------

print("\nCreating Chroma vector database...")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(VECTOR_DB_FOLDER),
    collection_name="college_documents"
)


print("\n-----------------------------")
print("Vector database created successfully!")
print("Location:", VECTOR_DB_FOLDER)
print("-----------------------------")