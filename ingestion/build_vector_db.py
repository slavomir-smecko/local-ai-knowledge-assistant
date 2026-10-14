import logging

import chromadb
from sentence_transformers import SentenceTransformer

from config import (
    VECTOR_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)

from ingestion.ingest import process_documents


logger = logging.getLogger(__name__)


def build_database():

    logger.info("Loading embedding model")

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    logger.info("Loading documents")

    chunks = process_documents()

    if not chunks:
        raise Exception(
            "No documents found"
        )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        chunk["metadata"]
        for chunk in chunks
    ]

    logger.info(
        "Creating embeddings for %s chunks",
        len(texts)
    )

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_PATH)
    )

    # Remove the existing collection so the database
    # can be rebuilt cleanly without duplicate IDs.
    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )

        logger.info(
            "Existing collection '%s' deleted",
            COLLECTION_NAME
        )

    except Exception:
        logger.info(
            "Collection '%s' does not exist yet",
            COLLECTION_NAME
        )

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    ids = [
        str(i)
        for i in range(len(texts))
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    logger.info(
        "Vector database created with %s documents",
        len(texts)
    )


if __name__ == "__main__":

    from logging_config import setup_logging

    setup_logging()

    build_database()

