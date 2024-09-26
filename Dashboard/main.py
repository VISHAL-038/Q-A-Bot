import os
import warnings
from RAG.app import PDF_RAG
from PyPDF2 import PdfReader
warnings.filterwarnings("ignore")


def find_path():
    for filename in os.listdir("user_documents"):
        if filename.endswith(".pdf"):
            file_path = os.path.join("user_documents", filename)
            return file_path
    if not file_path:
        print("No pdf found")
        return None

def upload_index(): 
    pdf_retriever = PDF_RAG(pdf_path=find_path())
    pdf_text = pdf_retriever.load_pdf()
    chunks = pdf_retriever.split_text_into_chunks(pdf_text)
    pdf_retriever.create_embeddings(chunks)
    pdf_retriever.set_prompt_template()

    return pdf_retriever

