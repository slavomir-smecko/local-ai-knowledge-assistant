import logging

import rag.startup as startup

from config import (
    SEARCH_K,
    TOP_K,
    MAX_DISTANCE
)


logger = logging.getLogger(__name__)


def retrieve_context(question):

    logger.info(
        "Creating query embedding"
    )


    if startup.embedding_model is None:
        raise RuntimeError(
            "Embedding model not initialized"
        )


    if startup.collection is None:
        raise RuntimeError(
            "Vector database collection not initialized"
        )


    query_embedding = startup.embedding_model.encode(
        question
    )


    results = startup.collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=SEARCH_K,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )


    documents = results.get(
        "documents",
        [[]]
    )[0]


    metadata = results.get(
        "metadatas",
        [[]]
    )[0]


    distances = results.get(
        "distances",
        [[]]
    )[0]


    logger.info(
        "Chroma returned %s candidates",
        len(documents)
    )


    #
    # Filter weak matches
    # Remove duplicate chunks
    #

    unique_chunks = []

    seen_chunks = set()


    for index, (
        document,
        meta,
        distance
    ) in enumerate(
        zip(
            documents,
            metadata,
            distances
        )
    ):

        source = meta.get(
            "source",
            "unknown"
        )


        logger.info(
            "Candidate %s | distance=%.3f | %s",
            index + 1,
            distance,
            source
        )


        if distance > MAX_DISTANCE:

            logger.info(
                "Rejected candidate %s (distance too high)",
                index + 1
            )

            continue


        cleaned_document = document.strip()


        if cleaned_document in seen_chunks:

            logger.info(
                "Rejected candidate %s (duplicate chunk)",
                index + 1
            )

            continue


        seen_chunks.add(
            cleaned_document
        )


        unique_chunks.append(
            {
                "document": cleaned_document,
                "metadata": meta,
                "distance": distance
            }
        )


    #
    # Keep best TOP_K chunks
    #

    selected_chunks = unique_chunks[:TOP_K]


    #
    # Build context
    #

    context = ""

    sources = []

    seen_sources = set()


    for index, item in enumerate(selected_chunks):

        document = item["document"]

        meta = item["metadata"]

        distance = item["distance"]


        source = meta.get(
            "source",
            "unknown"
        )


        context += f"""
SOURCE:
{source}

DOCUMENT:
{document}

---
"""


        #
        # Return unique source files only
        #

        if source not in seen_sources:

            sources.append(
                source
            )

            seen_sources.add(
                source
            )


        logger.info(
            "Selected chunk %s | distance=%.3f | %s",
            index + 1,
            distance,
            source
        )


    logger.info(
        "Retrieved %s chunks from %s candidates (TOP_K=%s, MAX_DISTANCE=%.2f, SOURCES=%s)",
        len(selected_chunks),
        len(documents),
        TOP_K,
        MAX_DISTANCE,
        len(sources)
    )


    return context, sources
