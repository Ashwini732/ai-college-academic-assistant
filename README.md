# AI-Based College Academic Assistant

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd ai-college-academic-assistant
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains the required Python libraries, so you do not need to install them individually.

### 4. Create the `.env` File

Create a `.env` file in the project root directory.

Add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit or push the `.env` file to GitHub.

### 5. Add the Documents

The academic PDF files are available in the `data` directory.

Keep the existing folder structure unchanged:

```text
data/
├── regulations/
├── examinations/
├── syllabus/
├── internship/
├── projects/
├── academic_calendar/
└── faq/
```

### 6. Run the Existing Files

Run the files in the following order:

#### Step 1 — Load Documents

```bash
python src/load_documents.py
```

#### Step 2 — Split Documents

```bash
python src/split_documents.py
```

#### Step 3 — Create Embeddings

Run the embedding-generation file/notebook provided in the repository.

**Current project progress is completed up to the `create_embeddings` stage.**

The next person working on the project should continue from the stage after embedding generation.

---

## Required Software

Make sure you have:

* Python 3.10+
* Git
* VS Code (recommended)

Python dependencies are already listed in:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## Git Workflow for Team Members

Create your own branch before making changes:

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

Then create a Pull Request to the `main` branch.

### Important

* Do not work directly on `main`.
* Do not commit `.env`.
* Do not commit `.venv`.
* Do not modify the existing document folders unnecessarily.
* Pull the latest changes before starting your work.

---

## Current Status

Completed:

```text
Document Loading
       ↓
Document Splitting
       ↓
Create Embeddings
```

**Next: Continue from the vector database / retrieval stage.**
