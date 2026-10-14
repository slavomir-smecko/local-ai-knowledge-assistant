from rag.retriever import retrieve_context


def test_chroma_retrieval():

    context, sources = retrieve_context(
        "What is RAG?"
    )

    assert len(context) > 0
    assert len(sources) > 0
