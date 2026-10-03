from load_documents import documents
from langchain_text_splitters import RecursiveCharacterTextSplitter


print("\nTotal documents/pages loaded:", len(documents))


# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# Split all documents
# This includes both PDFs and website content
chunks = text_splitter.split_documents(documents)


print("Total chunks created:", len(chunks))


# Display first 3 chunks
print("\n--- Sample Chunks ---")

for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i + 1}")

    print("Source:", chunk.metadata.get("source"))
    print("Source File:", chunk.metadata.get("source_file"))
    print("Page:", chunk.metadata.get("page", "N/A"))

    print("Text:")
    print(chunk.page_content[:500])