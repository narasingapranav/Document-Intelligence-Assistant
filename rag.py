from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
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
# GET USER VECTORSTORE
# -------------------------
def get_vectorstore(uid):
    return Chroma(
        collection_name=uid,
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

# -------------------------
# CREATE VECTOR DATABASE (PER USER)
# -------------------------
def make_emb(pdf_path, uid):

    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        if not pages:
            raise ValueError("No pages found in PDF.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(pages)

        chunks = [
            chunk for chunk in chunks
            if chunk.page_content and chunk.page_content.strip()
        ]

        if not chunks:
            raise ValueError("No valid text extracted from PDF.")

        for chunk in chunks:
            chunk.metadata = {
                k: v for k, v in chunk.metadata.items()
                if v is not None
            }

        vectorstore = get_vectorstore(uid)

        vectorstore.add_documents(chunks)

        print("✅ Embeddings stored for user:", uid)

        return True

    except Exception as e:
        print("\n❌ ERROR DURING EMBEDDING CREATION")
        traceback.print_exc()
        print("Error:", e)
        return False


# -------------------------
# SEARCH
# -------------------------
def search_docs(query, uid, k=3):

    vectorstore = get_vectorstore(uid)
    return vectorstore.similarity_search(query, k=k)


# -------------------------
# RAG QA
# -------------------------
def ask_question(question, uid):

    try:
        docs = search_docs(question, uid)

        if not docs:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Rules:
1. Answer only from the provided context.
2. If not found, say: "I don't know based on the provided documents."
3. Do not use outside knowledge.
"""

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": [
                {
                    "page": d.metadata.get("page", "Unknown"),
                    "source": d.metadata.get("source", "Unknown")
                }
                for d in docs
            ]
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }