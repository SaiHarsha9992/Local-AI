# ingest.py

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def ingest_documents(folder="docs"):
    documents = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif file.endswith(".txt"):
            loader = TextLoader(path)
        else:
            continue
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embedding = OllamaEmbeddings(model="mistral")  # Default model for embedding
    db = Chroma.from_documents(chunks, embedding=embedding, persist_directory="db")
    db.persist()
    print(f"✅ Ingested {len(chunks)} chunks into ChromaDB.")

if __name__ == "__main__":
    ingest_documents()

Create a dark-themed PowerPoint presentation titled “Mastering Core Java: From Basics to OOP” with a modern developer-friendly style, suitable for a 1.5-hour session. Use a dark background (e.g., dark gray or black) and white or light gray text with accent colors in blue or green. Font style should resemble “GhostCoder” aesthetics (monospaced font for code, clean sans-serif for headings and content).

Presentation should include the following 23 slides:
Slide 1: Title Slide
Title: Mastering Core Java: From Basics to OOP
Subtitle: Presenter Name, Date, Organization







