from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import shutil

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -------------------------
# CREATE / RESET VECTOR DB
# -------------------------
def make_emb(path):

    # 🔥 CLEAR OLD DATABASE (IMPORTANT FIX)
    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")

    pdf = PyPDFLoader(path)
    pages = pdf.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(pages)

    if not chunks:
        raise ValueError("No text extracted from PDF")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    print("✅ Embeddings created and stored in ChromaDB")


# -------------------------
# SEARCH
# -------------------------
def search_docs(query):

    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return db.similarity_search(query, k=3)


# -------------------------
# RAG ANSWER
# -------------------------
def ask_question(question):

    docs = search_docs(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    response = llm.invoke(f"""
Use the context below to answer.

Context:
{context}

Question:
{question}
""")

    sources = [
        {
            "page": doc.metadata.get("page"),
            "source": doc.metadata.get("source")
        }
        for doc in docs
    ]

    return {
        "answer": response.content,
        "sources": sources
    }