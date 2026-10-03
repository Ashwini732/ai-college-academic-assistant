import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Load environment variables
load_dotenv()

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_FOLDER / "data"
VECTOR_DB_FOLDER = PROJECT_FOLDER / "vector_db"

all_documents = []

# --- A. Load PDF Documents ---
print("Loading PDF documents from data folder...")
for pdf_path in DATA_FOLDER.glob("*.pdf"):
    print(f"  Loading PDF: {pdf_path.name}")
    try:
        loader = PyPDFLoader(str(pdf_path))
        pdf_docs = loader.load()
        for doc in pdf_docs:
            doc.metadata["source_file"] = pdf_path.name
            doc.metadata["source_type"] = "pdf"
        all_documents.extend(pdf_docs)
    except Exception as e:
        print(f"  Failed to load {pdf_path.name}: {e}")

# --- B. Load College Website Pages ---
# Key targeted website URLs for NMAMIT covering academics, placements, hostels, etc.
WEBSITE_URLS = [
    "https://nitte.edu.in/nmamit/index.php",
    "https://nitte.edu.in/nmamit/placement.php#2025-26",
    "https://nitte.edu.in/nmamit/hostels.php",
    "https://nitte.edu.in/nmamit/auditorium.php",
    "https://nitte.edu.in/nmamit/commercial-units.php",
    "https://nitte.edu.in/nmamit/"
    
]

print("\nLoading Website pages...")
for url in WEBSITE_URLS:
    try:
        print(f"  Fetching web page: {url}")
        web_loader = WebBaseLoader(url)
        web_docs = web_loader.load()
        for doc in web_docs:
            doc.metadata["source_file"] = url
            doc.metadata["source_type"] = "web"
        all_documents.extend(web_docs)
    except Exception as e:
        print(f"  Failed to load {url}: {e}")

print(f"\nTotal raw documents loaded: {len(all_documents)}")

# --- C. Document Chunking ---
print("\nSplitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(all_documents)
print(f"Total chunks created: {len(chunks)}")

# --- D. Create & Store Embeddings in ChromaDB ---
print("\nLoading embedding model (BAAI/bge-small-en-v1.5)...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

print(f"Saving vector database to {VECTOR_DB_FOLDER}...")
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(VECTOR_DB_FOLDER),
    collection_name="college_documents"
)

print("\nVector database successfully created and saved!")