# AI-Based College Academic Assistant

An AI-based academic assistant designed to help college students access academic information, search college documents, answer academic questions, and create personalized study plans.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd ai-college-academic-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` File

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit `.env` to GitHub.

### 5. Add Documents

Place the required PDF documents inside the `data/` folder.

## Create the Vector Database

Run:

```bash
python src/create_embeddings.py
```

This automatically:

1. Loads the PDF and website documents.
2. Splits the documents into chunks.
3. Creates embeddings using `BAAI/bge-small-en-v1.5`.
4. Creates the Chroma vector database.

Current result:

```text
1292 document chunks
```

The vector database is created in:

```text
vector_db/
```

## Project Structure

```text
ai-college-academic-assistant/
│
├── data/
│   └── academic documents
│
├── src/
│   ├── load_documents.py
│   ├── split_documents.py
│   └── create_embeddings.py
│
├── vector_db/
├── requirements.txt
├── README.md
└── .gitignore
```

## Git Workflow

Create a separate branch:

```bash
git checkout -b feature/your-feature-name
```

Example:

```bash
git checkout -b feature/rag-retrieval
```

After making changes:

```bash
git add .
git commit -m "Add RAG retrieval"
git push -u origin feature/rag-retrieval
```

Then create a Pull Request to `main`.

## Important

* Do not work directly on `main`.
* Do not commit `.env`.
* Do not commit `.venv`.
* Do not commit `vector_db/`.
* Pull the latest changes before starting work.

## Current Progress

```text
PDFs + Website
      ↓
Document Loading       ✓
      ↓
Document Splitting     ✓
      ↓
1292 Chunks            ✓
      ↓
BGE Embeddings         ✓
      ↓
Chroma Vector Database ✓
```

### Next Step

```text
Chroma Vector Database
          ↓
       Retriever
          ↓
      RAG Pipeline
          ↓
          LLM
```
