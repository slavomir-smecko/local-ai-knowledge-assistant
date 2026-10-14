from rag.engine import ask


def test_full_rag_pipeline():

    result = ask(
        "What is RAG?"
    )

    assert "answer" in result
    assert len(result["sources"]) > 0
