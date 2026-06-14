import os
import streamlit as st
from rag import make_emb, ask_question
from auth import auth
from db import users

st.set_page_config(
    page_title="Document Intelligence Assistant",
    page_icon="📄",
    layout="wide"
)

# -----------------------
# SESSION STATE INIT
# -----------------------
if "processed" not in st.session_state:
    st.session_state.processed = False

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "db_ready" not in st.session_state:
    st.session_state.db_ready = False

if "user" not in st.session_state:
    st.session_state.user = None

if "uid" not in st.session_state:
    st.session_state.uid = None


# -----------------------
# SIDEBAR
# -----------------------
with st.sidebar:
    st.title("📄 RAG Chatbot")

    if st.session_state.user:
        st.success("Logged In")

        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.uid = None
            st.session_state.processed = False
            st.session_state.db_ready = False
            st.session_state.messages = []
            st.rerun()

    st.markdown("""
    ### Steps
    1. Upload a PDF  
    2. Process document  
    3. Ask questions  

    **Powered by**
    - LangChain
    - ChromaDB
    - HuggingFace Embeddings
    - Gemini
    - Streamlit
    """)


# -----------------------
# LOGIN PAGE
# -----------------------
st.title("📄 Document Intelligence Assistant")
st.caption("Upload a PDF and chat with your document")

# IMPORTANT: show login if not logged in
if st.session_state.user is None:

    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)

                uid = user["localId"]

                users.update_one(
                    {"uid": uid},
                    {
                        "$set": {
                            "uid": uid,
                            "email": email
                        }
                    },
                    upsert=True
                )

                st.session_state.user = user
                st.session_state.uid = uid

                st.rerun()

            except Exception:
                st.error("Invalid credentials")

    with col2:
        if st.button("Register"):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Account created. Please login.")
            except Exception as e:
                st.error(str(e))

    st.stop()


# -----------------------
# SAFE UID ACCESS
# -----------------------
if st.session_state.user is None:
    st.error("Session expired. Please login again.")
    st.stop()

uid = st.session_state.uid


# -----------------------
# FILE UPLOAD
# -----------------------
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:

    # reset state if new file
    if st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        st.session_state.processed = False
        st.session_state.db_ready = False
        st.session_state.messages = []

    st.success("✅ PDF uploaded successfully!")

    st.info(f"""
    **File Name:** {uploaded_file.name}  
    **Size:** {uploaded_file.size / 1024:.2f} KB
    """)

    # -----------------------
    # PROCESS PDF
    # -----------------------
    if not st.session_state.processed:

        if st.button("🚀 Process PDF"):

            os.makedirs("uploads", exist_ok=True)

            pdf_path = os.path.join("uploads", uploaded_file.name)

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Creating embeddings..."):
                success = make_emb(pdf_path, uid)

            if success:
                st.session_state.processed = True
                st.session_state.db_ready = True
                st.session_state.messages = []

                st.success("✅ PDF processed successfully!")
                st.rerun()

            else:
                st.error("❌ Failed to process PDF")


# -----------------------
# CHAT INTERFACE
# -----------------------
if st.session_state.db_ready:

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask a question about the document...")

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Thinking..."):
            try:
                result = ask_question(question, uid)
            except Exception as e:
                st.error(f"RAG error: {e}")
                result = {"answer": "Error occurred", "sources": []}

        answer = result["answer"]

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)

            with st.expander("📚 Sources"):
                for source in result["sources"]:
                    page = source.get("page") if isinstance(source, dict) else None

                    page_text = (
                        f"Page {int(page) + 1}"
                        if isinstance(page, (int, str)) and str(page).isdigit()
                        else "Unknown Page"
                    )

                    st.write(f"📄 {source['source']} | {page_text}")

else:
    st.info("👆 Upload a PDF to get started.")