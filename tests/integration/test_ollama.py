from rag.llm import ask_llm


def test_ollama_response():

    answer = ask_llm(
        "What is this?",
        "This is a RAG assistant."
    )

    assert len(answer) > 0
