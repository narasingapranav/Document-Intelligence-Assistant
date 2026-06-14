import os
import streamlit as st
from rag import make_emb, ask_question
from auth import login, register
from db import users

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Document Intelligence Assistant",
    page_icon="📄",
    layout="wide"
)

# -----------------------
# SESSION STATE INIT
# -----------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "uid" not in st.session_state:
    st.session_state.uid = None

if "processed" not in st.session_state:
    st.session_state.processed = False

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "db_ready" not in st.session_state:
    st.session_state.db_ready = False


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
# TITLE
# -----------------------
st.title("📄 Document Intelligence Assistant")
st.caption("Upload a PDF and chat with your document")


# -----------------------
# LOGIN / REGISTER PAGE
# -----------------------
if st.session_state.user is None:

    st.subheader("🔐 Login / Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    # LOGIN
    with col1:
        if st.button("Login"):
            res = login(email, password)

            if "localId" in res:
                st.session_state.user = res
                st.session_state.uid = res["localId"]

                # store user in MongoDB
                users.update_one(
                    {"uid": st.session_state.uid},
                    {"$set": {"uid": st.session_state.uid, "email": email}},
                    upsert=True
                )

                st.success("Login successful")
                st.rerun()

            else:
                st.error(res.get("error", {}).get("message", "Login failed"))

    # REGISTER
    with col2:
        if st.button("Register"):
            res = register(email, password)

            if "localId" in res:
                st.success("Account created. Please login.")
            else:
                st.error(res.get("error", {}).get("message", "Signup failed"))

    st.stop()


# -----------------------
# SAFE UID CHECK
# -----------------------
if st.session_state.user is None or st.session_state.uid is None:
    st.error("Session expired. Please login again.")
    st.stop()

uid = st.session_state.uid


# -----------------------
# FILE UPLOAD
# -----------------------
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:

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

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

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
                    page = source.get("page")

                    page_text = (
                        f"Page {int(page) + 1}"
                        if isinstance(page, (int, str)) and str(page).isdigit()
                        else "Unknown Page"
                    )

                    st.write(f"📄 {source.get('source', 'Unknown')} | {page_text}")

else:
    st.info("👆 Upload a PDF to get started.")