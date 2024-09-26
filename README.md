# Q-A-Bot with Retrieval-Augmented Generation (RAG)

Q-A-Bot is a question-answering bot that extracts answers from a PDF document uploaded by the user. Built using Streamlit for the frontend and various libraries for document processing, Q-A-Bot provides an interactive way to query information from PDFs.

## Features

- Upload a PDF document to extract information.
- Ask questions related to the content of the PDF.
- Answers are generated using the Cohere API for natural language processing
## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Application](#running-the-application)

## Introduction

This project demonstrates a QA system that answers user queries based on document content. It integrates a RAG model that uses document embeddings for retrieval and a generative model (like Cohere API) to generate answers.

The system includes:

- A backend that manages document embedding and retrieval using Pinecone DB.
- A frontend interface built using Streamlit for real-time user interaction.

## Features

- Upload PDF documents and extract content.
- Store and retrieve document embeddings using a vector database.
- Generate coherent, contextually relevant answers using a generative model.
- Real-time query answering with the ability to view the relevant document segments.

## Requirements

To run this project locally, you need the following dependencies:

- Python 3.8 or higher
- Streamlit for the frontend
- Pinecone for document retrieval
- Cohere API (or an alternative generative model)
- Docker (optional, for containerization)
- Additional Python libraries (see `requirements.txt`)

## Installation

Follow these steps to set up the QA bot on your local machine:

1. **Install the required dependencies**: It's recommended to create a virtual environment first:

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # For Windows: myenv\Scripts\activate
   
Then, install the dependencies:

    ```bash
    pip install -r requirements.txt

### Configure API Keys

You'll need API keys for Pinecone and Cohere (or the generative model of your choice). Create a `.env` file in the root directory with the following content:

      ```makefile
      PINECONE_API_KEY=your-pinecone-api-key
      COHERE_API_KEY=your-cohere-api-key

## Usage

### Uploading Documents and Asking Questions

Once the application is running, you can upload a PDF document from the frontend interface. After uploading the document, ask a question related to its content. The system will retrieve relevant information from the document and generate a response using the RAG model.

### Running the Application

To run the QA bot on your local machine:

```bash
streamlit run app.py

