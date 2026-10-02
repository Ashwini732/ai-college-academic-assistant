from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"

documents = []

for pdf_file in DATA_FOLDER.glob("*.pdf"):
    print(f"Loading: {pdf_file.name}")

    loader = PyPDFLoader(str(pdf_file))
    docs = loader.load()

    documents.extend(docs)

print("\n-----------------------------")
print("Documents loaded successfully!")
print("Total pages loaded:", len(documents))
print("-----------------------------")

for doc in documents[:3]:
    print("\nSource:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page"))
    print("Text preview:")
    print(doc.page_content[:500])