from pathlib import Path
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"

documents = []

for pdf_file in DATA_FOLDER.glob("*.pdf"):
    print(f"Loading PDF: {pdf_file.name}")

    loader = PyPDFLoader(str(pdf_file))
    docs = loader.load()

    documents.extend(docs)

# Add your website URLs to this list
urls = [
    "https://share.google/dLAHGu4kLMYeyPIpv",
]

for url in urls:
    print(f"Loading URL: {url}")
    loader = WebBaseLoader(url)
    docs = loader.load()
    documents.extend(docs)

print("\n-----------------------------")
print("Documents loaded successfully!")
print("Total pages/documents loaded:", len(documents))
print("-----------------------------")

for doc in documents[:3]:
    print("\nSource:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page", "N/A"))
    print("Text preview:")
    print(doc.page_content[:500])