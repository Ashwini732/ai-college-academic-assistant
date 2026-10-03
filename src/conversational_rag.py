import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# 1. Environment Setup
load_dotenv()

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
VECTOR_DB_FOLDER = PROJECT_FOLDER / "vector_db"

# 2. Embedding Model & Vector DB
print("Loading embeddings and vector store...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vector_store = Chroma(
    persist_directory=str(VECTOR_DB_FOLDER),
    embedding_function=embeddings,
    collection_name="college_documents"
)
retriever = vector_store.as_retriever(search_kwargs={"k": 6})

# 3. OpenRouter LLM Setup
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env file!")

llm = ChatOpenAI(
    model_name="openai/gpt-4o-mini",
    openai_api_key=openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0
)

# 4. Standalone Contextualizer Prompt (Rephrases follow-ups using chat history)
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 5. QA Prompt Template
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI Academic Assistant. Answer using ONLY the context provided. If information is missing, state that it's unavailable.\n\nContext:\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

def format_docs(docs):
    seen = set()
    chunks = []
    for doc in docs:
        content = doc.page_content.strip()
        if content not in seen:
            seen.add(content)
            chunks.append(content)
    return "\n\n".join(chunks)

# 6. Interactive Chat Loop
def start_chat():
    chat_history = []
    print("\n==================================================")
    print("AI Academic Assistant - Conversational Mode")
    print("Type 'exit' or 'quit' to end the session.")
    print("==================================================\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("Session ended.")
            break

        # A. Rephrase question if follow-up
        if chat_history:
            rephrase_chain = contextualize_q_prompt | llm | StrOutputParser()
            search_query = rephrase_chain.invoke({"input": user_input, "chat_history": chat_history})
        else:
            search_query = user_input

        # B. Retrieve docs & Generate Answer
        retrieved_docs = retriever.invoke(search_query)
        context = format_docs(retrieved_docs)

        qa_chain = qa_prompt | llm | StrOutputParser()
        response = qa_chain.invoke({
            "input": user_input,
            "chat_history": chat_history,
            "context": context
        })

        print(f"\nAI: {response}\n" + "-"*50)

        # C. Store turns in memory
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

if __name__ == "__main__":
    start_chat()