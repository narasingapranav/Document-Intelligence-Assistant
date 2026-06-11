# 📄 Document Intelligence Assistant

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions about their content.

The application uses LangChain, ChromaDB, Hugging Face Embeddings, and Google's Gemini model to provide accurate, context-aware answers with source citations.

---

## 🚀 Features

- Upload PDF documents
- Automatic document chunking
- Semantic search using vector embeddings
- ChromaDB vector database
- Gemini-powered question answering
- Source page citations
- Interactive chat interface using Streamlit

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python
- LangChain

### Vector Database
- ChromaDB

### Embeddings
- Hugging Face Embeddings
- sentence-transformers/all-MiniLM-L6-v2

### Large Language Model
- Gemini 2.5 Flash

---

## 📂 Project Structure

```text
.
├── app.py
├── rag.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── uploads/        # Ignored
├── chroma_db/      # Ignored
└── rag/            # Virtual Environment (Ignored)
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd rag-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv rag
```

### 3. Activate Virtual Environment

#### Windows

```bash
rag\Scripts\activate
```

#### Linux / macOS

```bash
source rag/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
GOOGLE_API_KEY=your_google_api_key
```

You can obtain a Gemini API key from:

https://aistudio.google.com/app/apikey

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 📖 How It Works

1. User uploads a PDF document.
2. The PDF is loaded using PyPDFLoader.
3. The document is split into smaller chunks.
4. Hugging Face Embeddings generate vector representations.
5. Chunks are stored in ChromaDB.
6. User asks a question.
7. Relevant chunks are retrieved using semantic search.
8. Gemini generates an answer based on the retrieved context.
9. Sources and page references are displayed.

---

## 🏗️ Architecture

```text
PDF
 ↓
PyPDFLoader
 ↓
Text Chunking
 ↓
Hugging Face Embeddings
 ↓
ChromaDB
 ↓
Retriever
 ↓
Gemini 2.5 Flash
 ↓
Answer + Citations
```

---

## 💬 Example Questions

- What is the main topic of this document?
- Summarize chapter 1.
- Explain the key concepts discussed.
- What conclusions are presented in the document?
- List the important points from this report.

---

## 🔮 Future Improvements

- Multiple PDF support
- Conversational memory
- Chat history persistence
- PDF preview inside the application
- Export chat history
- Hybrid search (keyword + semantic search)
- Cloud deployment

---

## 👨‍💻 Author

Built as a Generative AI and RAG project using:

- LangChain
- ChromaDB
- Hugging Face Embeddings
- Gemini
- Streamlit

---