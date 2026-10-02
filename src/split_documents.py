from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Find the data folder
DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"

documents = []

# Load all PDF files from data folder
for pdf_file in DATA_FOLDER.glob("*.pdf"):
    print(f"Loading: {pdf_file.name}")

    loader = PyPDFLoader(str(pdf_file))
    docs = loader.load()

    # Store the original filename in metadata
    for doc in docs:
        doc.metadata["source_file"] = pdf_file.name

    documents.extend(docs)


print("\nTotal pages loaded:", len(documents))


# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Split documents
chunks = text_splitter.split_documents(documents)


print("Total chunks created:", len(chunks))


# Display first 3 chunks
print("\n--- Sample Chunks ---")

for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i + 1}")
    print("Source:", chunk.metadata.get("source_file"))
    print("Page:", chunk.metadata.get("page"))
    print("Text:")
    print(chunk.page_content[:500])