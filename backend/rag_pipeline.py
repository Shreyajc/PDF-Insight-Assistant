from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import (
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    FAISS_PATH,
)

from backend.llm import load_llm


# -----------------------------
# Split PDF into chunks
# -----------------------------
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    return splitter.split_documents(documents)


# -----------------------------
# Create FAISS
# -----------------------------
def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    db = FAISS.from_documents(
        chunks,
        embeddings
    )

    db.save_local(FAISS_PATH)

    return db


# -----------------------------
# Load FAISS
# -----------------------------
def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


# -----------------------------
# Retriever
# -----------------------------
def get_retriever(db):

    return db.as_retriever(

        search_type="mmr",

        search_kwargs={
            "k": 5,
            "fetch_k": 20,
        }

    )


# -----------------------------
# Ask Question
# -----------------------------
def ask_question(question, retriever):

    docs = retriever.invoke(question)

    context = ""

    seen = set()

    for doc in docs:

        text = doc.page_content.strip()

        if text in seen:
            continue

        seen.add(text)

        context += text[:900] + "\n\n"

    prompt = f"""
You are an expert assistant for PDF question answering.

Answer ONLY using the context below.

If the answer is not available, say:

"I couldn't find that information in the uploaded PDF."

Write complete sentences.

Do not answer in one word.

Explain clearly in 3-5 sentences.

Mention important names, methods, datasets and conclusions whenever they are present in the document.

Do not answer in one word.

Context:
{context}

Question:
{question}

Answer:
"""

    answer = load_llm(prompt)
    return answer, docs