import streamlit as st
import os
import shutil
from main import upload_index

upload_folder = "user_documents"


def save_uploaded_file(uploaded_file, upload_folder):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, uploaded_file.name)

    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None


if "files_uploaded" not in st.session_state:
    shutil.rmtree(upload_folder)
    os.makedirs(upload_folder)
    st.session_state["files_uploaded"] = False

if "qa_history" not in st.session_state:
    st.session_state["qa_history"] = []
st.sidebar.title("Upload Documents")
uploaded_file = st.sidebar.file_uploader(
    "Upload a document (PDF, DOCX, PPTX, etc.)", type=["pdf", "docx", "pptx"]
)

if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file, upload_folder)
    retriever = upload_index()
    if file_path:
        st.session_state["files_uploaded"] = True
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")
    else:
        st.sidebar.error("File could not be saved.")
else:
    st.sidebar.info("Please upload a document.")

st.title("Ask Questions")

if "files_uploaded" in st.session_state and st.session_state["files_uploaded"]:
    question = st.text_input("Ask a question about the document:")
    if question:
        answer = retriever.generate_answer(question + " context_history: " + " ".join([qa[0] for qa in st.session_state["qa_history"][-3:]]))
        st.session_state["qa_history"].append((question, answer))
        for q, a in st.session_state["qa_history"][::-1]:
            st.write(f"**Q:** {q}")
            st.write(f"**A:** {a}")
            st.write("---")
else:
    st.write("Upload a document first to ask questions.")
# shutil.rmtree(upload_folder)
# os.makedirs(upload_folder)