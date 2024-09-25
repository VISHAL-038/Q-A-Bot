import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Cohere

class PDF_RAG:
    def __init__(self, pdf_path, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.pdf_path = pdf_path
        self.model_name = model_name
        self.vectorstore = None
        self.retriver = None
        self.prompt = None
    
    def load_pdf(self):
        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_text = ""
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            return pdf_text
    
    def split_text_into_chunks(self,text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap=200,
            length_function=len,
            separators=['\n\n', ' ', '']
        )
        return text_splitter.split_text(text=text)
    
    def create_embeddings(self, chunks):
        embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
        self.vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
        self.retriver = self.vectorstore.as_retriver(search_type="similarit",search_kwargs={"k":2})
    
    def set_propmpt_template(self):
        prompt_template = """Answer the question as precisely as possible using the provided context. 
                            If the answer is not contained in the context, say "answer not available in context" 
                            \n\nContext: \n {context}?\nQuestion: \n {question} \nAnswer:"""
        self.prompt = PromptTemplate.from_template(template=prompt_template)
    
    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def generate_answer(self, question):
        if not self.retriver:
            raise ValueError("Retriver not initialized. Run the 'create_embeddings' method first.")
        
        load_dotenv()  #load API keys from .env file
        cohere_llm = Cohere(model="command", temperature=0.1, cohere_api_key=os.getenv('COHERE_API_KEY'))

        rag_chain =(
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | cohere_llm
            | StrOutputParser()
        )

        return rag_chain.invoke(question)