import logging
from typing import List, Dict

from fastapi import FastAPI
from pydantic import BaseModel, Field

from rag.startup import initialize_rag
from rag.engine import ask_question


logger = logging.getLogger(__name__)


app = FastAPI(
    title="AI Research Assistant API",
    version="0.1"
)


class QuestionRequest(BaseModel):

    question: str

    history: List[Dict] = Field(
        default_factory=list
    )


@app.on_event("startup")
def startup_event():

    logger.info(
        "Initializing RAG"
    )

    initialize_rag()


@app.post("/ask")
def ask(request: QuestionRequest):

    logger.info(
        "Received question request"
    )

    logger.info(
        "History received: %s messages",
        len(request.history)
    )

    result = ask_question(
        request.question,
        request.history
    )

    return result


@app.get("/health")
def health():

    return {
        "status": "ok"
    }
