# AI-Based College Academic Assistant

An AI-based academic assistant designed to help college students access academic information, search college documents, answer academic questions, and create personalized study plans.

## Project Overview

The system uses:

* Large Language Models (LLM)
* Retrieval-Augmented Generation (RAG)
* LangChain
* LangGraph
* Vector Database
* Embeddings
* External tools/APIs
* Simple user interface

The assistant is designed to work with official college academic documents such as regulations, examination guidelines, syllabus documents, internship guidelines, project guidelines, academic calendars, and FAQs.

## Main Features

### 1. Academic Question Answering

The assistant can answer questions related to college academics using the available college documents.

### 2. Document Search

The system retrieves relevant information from the college documents using RAG.

### 3. Conversational Questions

The assistant should be able to understand follow-up questions using conversational context.

### 4. Personalized Study Planner

Students can provide information such as:

* Subjects
* Available study time
* Examination date
* Study preferences

The assistant can then generate a personalized study plan.

### 5. Study Plan Modification

Students can request changes to an existing study plan.

### 6. Unknown Question Handling

If the required information cannot be found in the available college documents, the system should clearly indicate that the information is not available rather than generating unsupported information.

### 7. External Tool/API

The system will integrate at least one external tool or API, such as a calculator or calendar-related tool.

### 8. LangGraph Workflow

The planned workflow includes:

```text
User Question
      ↓
Question Analysis
      ↓
Document Retrieval
      ↓
Response Generation
      ↓
Response Review
      ↓
Final Answer
```

## RAG Pipeline

The document-based question answering system follows this pipeline:

```text
College PDFs
     ↓
Document Loading
     ↓
Text Extraction
     ↓
Text Chunking
     ↓
Embeddings
     ↓
Vector Database
     ↓
Retriever
     ↓
Relevant Context
     ↓
LLM
     ↓
Final Answer
```

## Project Structure

```text
ai-college-academic-assistant/
│
├── data/
│   ├── regulations/
│   ├── examinations/
│   ├── syllabus/
│   ├── internship/
│   ├── projects/
│   ├── academic_calendar/
│   └── faq/
│
├── src/
│   ├── load_documents.py
│   ├── split_documents.py
│   └── ...
│
├── vector_db/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies

* Python
* LangChain
* LangGraph
* ChromaDB
* Sentence Transformers
* PyPDF
* LLM API
* Streamlit

## Setup Instructions

### 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
```

Move into the project directory:

```bash
cd ai-college-academic-assistant
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Run the document loader

```bash
python src/load_documents.py
```

The document loading process will read the academic PDF files from the `data` directory.

## Current Development Status

### Completed

* [x] Project repository setup
* [x] College academic documents collected
* [x] Data directory created
* [x] PDF document loading
* [ ] Document chunking
* [ ] Embedding generation
* [ ] Vector database creation
* [ ] RAG pipeline
* [ ] LLM integration
* [ ] LangGraph workflow
* [ ] External tool/API integration
* [ ] Personalized study planner
* [ ] Study plan modification
* [ ] Streamlit UI
* [ ] Testing and evaluation

## Team Collaboration

Each team member should create a separate branch for their work.

Create a branch:

```bash
git checkout -b feature/your-feature-name
```

Example:

```bash
git checkout -b feature/rag-retrieval
```

After completing the feature:

```bash
git add .
git commit -m "Add RAG retrieval"
git push -u origin feature/rag-retrieval
```

Then create a Pull Request on GitHub for the team to review and merge.

## Important Notes

* Do not commit API keys or passwords.
* Do not commit the `.venv` folder.
* Do not commit generated vector databases unless the team specifically decides to version them.
* Keep the project structure consistent.
* Create a separate branch before working on a new feature.
* Pull the latest changes before starting new work.

## Team

This project is being developed as an academic project.

Contributors:

* Add team member names here.

## License

This project is intended for academic and educational purposes.
