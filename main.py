
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from rag import get_answer, initialize_rag_chain

class Question(BaseModel):
    question: str

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    initialize_rag_chain()

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API"}

@app.post("/ask")
def ask_question(question: Question):
    answer = get_answer(question.question)
    return {"answer": answer}
