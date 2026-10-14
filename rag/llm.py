import logging
import time
import os

import ollama

from config import LLM_MODEL


logger = logging.getLogger(__name__)


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)


logger.info(
    "Ollama client initialized with host: %s",
    OLLAMA_HOST
)


client = ollama.Client(
    host=OLLAMA_HOST
)


def ask_llm(
    question,
    history,
    context
):

    prompt = f"""
You are an AI Research Assistant.

Your task is to answer the user's current question using the retrieved knowledge base.

You have access to three separate inputs:

1. Conversation history
   - Used only to understand previous discussion.
   - It helps answer follow-up questions.
   - It is NOT a source of factual knowledge.

2. Retrieved documents
   - These are the primary source of truth.
   - Use them to answer factual questions.
   - Do not use outside knowledge.

3. Current user question
   - This is the question you must answer.


IMPORTANT RULES:

Knowledge usage:

- Use retrieved documents as the primary source.
- Do not use outside knowledge.
- Do not invent missing information.
- If the retrieved documents do not contain enough information, answer exactly:

"I don't know based on the provided documents."


Conversation history:

- Use previous conversation only when the user refers to earlier messages.
- Examples:
    "What did I ask before?"
    "Explain that again"
    "Compare it with the previous one"

- Do not treat previous assistant answers as factual evidence.
- Verify factual answers against retrieved documents whenever possible.


Reasoning:

- First identify what the user is asking.
- Check whether retrieved documents actually answer the question.
- Ignore documents that are only loosely related.
- Base important statements on retrieved evidence.
- Do not assume concepts are connected because:
    - they appear in the same documentation,
    - they were retrieved together,
    - they share keywords,
    - they are both n8n concepts.


Comparison questions:

When comparing two things:

1. Explain the purpose of each item separately.
2. Identify real similarities.
3. Identify real differences.
4. Only claim overlap when documents clearly support it.


Answer style:

- Be concise.
- Explain concepts in simple language.
- Use examples when useful.
- Prefer explanations over copying documentation.
- Combine information from multiple relevant documents.
- Avoid repeating identical information.


Conversation history:

{history}


Retrieved documents:

{context}


Current user question:

{question}


Now provide the answer.
"""


    logger.info(
        "Calling Ollama model: %s",
        LLM_MODEL
    )


    start_time = time.time()


    stream = client.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )


    answer = ""


    for chunk in stream:
        answer += chunk["message"]["content"]


    duration = time.time() - start_time


    logger.info(
        "LLM response completed in %.2f seconds",
        duration
    )


    return answer
