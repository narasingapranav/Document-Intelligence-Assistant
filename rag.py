from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

import os
import shutil
import traceback

# -------------------------
# LOAD ENVIRONMENT
# -------------------------
load_dotenv()

# -------------------------
# LLM
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# -------------------------
# EMBEDDING MODEL
# -------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

DB_PATH = "chroma_db"


# -------------------------
# CREATE VECTOR DATABASE
# -------------------------
def make_emb(pdf_path):

    try:
        # Remove old database
        if os.path.exists(DB_PATH):
            shutil.rmtree(DB_PATH)

        # Load PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        if not pages:
            raise ValueError("No pages found in PDF.")

        # Split text
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(pages)

        # Remove empty chunks
        chunks = [
            chunk
            for chunk in chunks
            if chunk.page_content and chunk.page_content.strip()
        ]

        if not chunks:
            raise ValueError("No valid text extracted from PDF.")

        # Clean metadata
        for chunk in chunks:
            chunk.metadata = {
                str(k): str(v)
                for k, v in chunk.metadata.items()
                if v is not None
            }

        print(f"Pages Loaded : {len(pages)}")
        print(f"Chunks Created: {len(chunks)}")

        # Create Chroma DB
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_PATH
        )

        print("✅ ChromaDB created successfully")

        return True

    except Exception as e:
        print("\n❌ ERROR DURING EMBEDDING CREATION")
        traceback.print_exc()
        print("Error:", e)
        return False


# -------------------------
# SEARCH DOCUMENTS
# -------------------------
def search_docs(query, k=3):

    if not os.path.exists(DB_PATH):
        raise ValueError("Vector database not found. Upload a PDF first.")

    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    docs = db.similarity_search(query, k=k)

    return docs


# -------------------------
# RAG QUESTION ANSWERING
# -------------------------
def ask_question(question):

    try:

        docs = search_docs(question)

        if not docs:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Rules:
1. Answer only from the provided context.
2. If the answer is not found in the context, reply:
   "I don't know based on the provided documents."
3. Do not use outside knowledge.
"""

        response = llm.invoke(prompt)

        sources = []

        for doc in docs:
            sources.append({
                "page": doc.metadata.get("page", "Unknown"),
                "source": doc.metadata.get("source", "Unknown")
            })

        return {
            "answer": response.content,
            "sources": sources
        }

    except Exception as e:
        traceback.print_exc()

        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }