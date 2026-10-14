import logging

from sentence_transformers import SentenceTransformer
import chromadb

from config import (
    VECTOR_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL
)

logger = logging.getLogger(__name__)


embedding_model = None
collection = None


def initialize_rag():

    global embedding_model
    global collection


    logger.info(
        "Loading embedding model"
    )

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )


    logger.info(
        "Connecting to Chroma"
    )

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_PATH)
    )


    collection = client.get_collection(
        COLLECTION_NAME
    )


    logger.info(
        "RAG initialization complete"
    )
