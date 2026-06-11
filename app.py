import os
import streamlit as st
from rag import make_emb, ask_question

st.set_page_config(
    page_title="Document Intelligence Assistant",
    page_icon="📄",
    layout="wide"
)

# -----------------------
# Session State
# -----------------------
if "processed" not in st.session_state:
    st.session_state.processed = False

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Sidebar
# -----------------------
with st.sidebar:
    st.title("📄 RAG Chatbot")

    st.markdown("""
    ### Steps
    1. Upload a PDF
    2. Process the document
    3. Ask questions

    **Powered by**
    - LangChain
    - ChromaDB
    - HuggingFace Embeddings
    - Gemini
    - Streamlit
    """)

# -----------------------
# Main UI
# -----------------------
st.title("📄 Document Intelligence Assistant")
st.caption("Upload a PDF and chat with your document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:

    # Reset state if new PDF uploaded
    if st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        st.session_state.processed = False
        st.session_state.messages = []

    st.success("✅ PDF uploaded successfully!")

    st.info(
        f"""
        **File Name:** {uploaded_file.name}

        **Size:** {uploaded_file.size / 1024:.2f} KB
        """
    )

    if not st.session_state.processed:

        if st.button("🚀 Process PDF"):

            os.makedirs("uploads", exist_ok=True)

            pdf_path = os.path.join(
                "uploads",
                uploaded_file.name
            )

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Creating embeddings..."):
                make_emb(pdf_path)

            st.session_state.processed = True

            st.success(
                "✅ PDF processed successfully! You can now ask questions."
            )

    # -----------------------
    # Chat Interface
    # -----------------------
    if st.session_state.processed:

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        question = st.chat_input(
            "Ask a question about the document..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):
                st.write(question)

            with st.spinner("Thinking..."):
                result = ask_question(question)

            answer = result["answer"]

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.chat_message("assistant"):
                st.write(answer)

                with st.expander("📚 Sources"):

                    for source in result["sources"]:

                        page = source.get("page")

                        page_text = (
                            f"Page {page + 1}"
                            if page is not None
                            else "Unknown Page"
                        )

                        st.write(
                            f"📄 {source['source']} | {page_text}"
                        )

else:
    st.info("👆 Upload a PDF to get started.")