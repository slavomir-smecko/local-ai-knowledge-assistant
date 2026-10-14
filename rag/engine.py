import logging

from rag.retriever import retrieve_context
from rag.llm import ask_llm


logger = logging.getLogger(__name__)


def ask_question(question, history=None):

    logger.info(
        "Processing question"
    )

    if history is None:
        history = []

    logger.info(
        "Received history with %s messages",
        len(history)
    )

    context, sources = retrieve_context(
        question
    )

    logger.info(
        "Retrieved %s sources",
        len(sources)
    )

    #
    # Build conversation history
    #

    history_text = ""

    if history:

        history_text = "Previous conversation:\n\n"

        for item in history:

            previous_question = item.get(
                "question",
                ""
            )

            previous_answer = item.get(
                "answer",
                ""
            )

            history_text += (
                f"User: {previous_question}\n"
                f"Assistant: {previous_answer}\n\n"
            )

    answer = ask_llm(
        question=question,
        history=history_text,
        context=context
    )

    logger.info(
        "Answer generated successfully"
    )

    return {
        "answer": answer,
        "sources": sources
    }
