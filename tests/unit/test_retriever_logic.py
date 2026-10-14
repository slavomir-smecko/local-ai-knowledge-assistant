def test_context_format():

    documents = [
        "RAG uses retrieval",
        "Embeddings create vectors"
    ]

    context = "\n".join(documents)

    assert "RAG" in context
    assert "Embeddings" in context
