from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# -----------------------------
# 1. Paths
# -----------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_FOLDER / "data"
VECTOR_DB_FOLDER = PROJECT_FOLDER / "vector_db"


# -----------------------------
# 2. Load PDF documents
# -----------------------------

documents = []

for pdf_file in DATA_FOLDER.glob("*.pdf"):
    print(f"Loading: {pdf_file.name}")

    loader = PyPDFLoader(str(pdf_file))
    docs = loader.load()

    for doc in docs:
        doc.metadata["source_file"] = pdf_file.name

    documents.extend(docs)


print("\nTotal pages loaded:", len(documents))


# -----------------------------
# 3. Split into chunks
# -----------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Total chunks created:", len(chunks))


# -----------------------------
# 4. Create embeddings
# -----------------------------

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

print("Embedding model loaded.")


# -----------------------------
# 5. Create Chroma database
# -----------------------------

print("\nCreating Chroma vector database...")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(VECTOR_DB_FOLDER),
    collection_name="college_documents"
)

print("\nVector database created successfully!")
print("Location:", VECTOR_DB_FOLDER)