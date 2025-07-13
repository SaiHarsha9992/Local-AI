# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama


app = FastAPI()
origins = [
    "https://local-ai-seven.vercel.app",  # your Vercel frontend
    "http://localhost:5173",              # optional, for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # ✅ list of domains
    allow_credentials=True,      # ✅ good for future auth support
    allow_methods=["*"],
    allow_headers=["*"],
)

# API request schema
class QuestionRequest(BaseModel):
    question: str
    model: str = "mistral"

@app.post("/ask")
def ask_question(req: QuestionRequest):
    # Load vector store
    embeddings = OllamaEmbeddings(model=req.model)
    vectordb = Chroma(persist_directory="db", embedding_function=embeddings)
    retriever = vectordb.as_retriever()

    # Load LLM
    llm = Ollama(model=req.model)
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Run query
    answer = chain.run(req.question)
    return {"answer": answer}
