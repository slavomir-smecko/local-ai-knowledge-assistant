# Local AI Knowledge Assistant

Web application name: AI Research Assistant

A local-first Retrieval-Augmented Generation (RAG) application for asking questions about a private document collection. It combines semantic search, locally hosted language models, a REST API, workflow automation, and a browser-based chat interface.

Built with **Python, FastAPI, ChromaDB, Sentence Transformers, Ollama, n8n, and Docker Compose**, this project demonstrates how a local AI assistant can retrieve information from documents, generate context-grounded answers, and maintain session-based conversation history.

## Overview

The assistant retrieves relevant document passages and supplies them as context to a local language model. The application separates document ingestion from question answering: documents are processed into a persistent vector database, and incoming questions search that existing database.

### Key features

- Local document ingestion, chunking, and embedding generation.
- Semantic retrieval using ChromaDB.
- Local language model inference through Ollama.
- FastAPI endpoints for question answering and health checks.
- n8n workflow orchestration through a webhook.
- Session-based conversation history managed by n8n.
- Browser-based chat interface served by Nginx.
- API and workflow execution logging for troubleshooting.
- Environment-based configuration for model settings, retrieval parameters, and service ports.

## Demo

The `screenshots/` directory contains visual examples of the application and its components.

Examples include:

- `screenshots/AI_Research_Assistant.mp4` — application demonstration.
- `screenshots/FastAPI.png` — API documentation.
- `screenshots/n8n_workflow.png` — workflow overview.
- `screenshots/docker_ps.png` — running containers.

## Architecture

The application consists of four main components.

**1. Document ingestion**

Source documents are loaded, split into overlapping chunks, converted into embeddings, and stored in ChromaDB. This is a separate preparation step rather than part of each question request.

**2. RAG backend**

FastAPI exposes the question-answering endpoint. The retrieval layer searches the existing ChromaDB collection for relevant passages, and the LLM integration sends the question and retrieved context to Ollama.

**3. Workflow orchestration**

n8n receives requests through a webhook, validates input, manages session history, calls the FastAPI backend, stores conversation data, and handles the response.

**4. Browser interface**

A lightweight HTML, CSS, and JavaScript frontend sends questions to the n8n webhook and displays the returned answers.

## Request lifecycle

When a user submits a question:

1. The browser sends the question and session identifier to the n8n webhook.
2. The workflow validates the request and retrieves available conversation history for that session.
3. n8n sends the question and history to the FastAPI `/ask` endpoint.
4. The backend embeds the question and searches the existing ChromaDB collection.
5. Relevant document passages are supplied to the configured Ollama model as context.
6. The generated answer and source information are returned to n8n.
7. The workflow records conversation data and returns the response to the browser.

### Document preparation and retrieval

Document preparation is separate from the request lifecycle:

1. Load supported source documents from `documents/`.
2. Split the text into chunks with configurable size and overlap.
3. Generate embeddings using Sentence Transformers.
4. Store the chunks and embeddings in ChromaDB.
5. At question time, embed the query and retrieve relevant stored chunks.

The persistent vector database is generated data and is excluded from version control. Rebuild it intentionally when the knowledge base changes.

## Technology stack

| Component | Technology |
|---|---|
| API | Python, FastAPI, Uvicorn |
| Retrieval | ChromaDB |
| Embeddings | Sentence Transformers |
| Local LLM inference | Ollama |
| Workflow automation | n8n |
| Frontend | HTML, CSS, JavaScript |
| Web server | Nginx |
| Containerization | Docker, Docker Compose |

## Features in detail

### Retrieval-augmented generation

- Document processing and chunking.
- Local embedding generation and persistent vector storage.
- Semantic retrieval with configurable search parameters.
- Distance-based relevance filtering.
- Selection of relevant passages for model context.
- Source information associated with answers.

### API

- `POST /ask` — question answering.
- `GET /health` — API health check.
- `/docs` — interactive Swagger UI.
- `/redoc` — ReDoc API documentation.

### n8n workflow

- Webhook-based request entry point.
- Request validation and session handling.
- Retrieval of conversation history.
- HTTP communication with the FastAPI backend.
- Conversation persistence.
- Workflow execution tracking and logging.

The primary n8n workflow is available in n8n/workflows/AI Research Assistant - RAG v1.0.json. It implements webhook-based request handling, input validation, session history retrieval, communication with the FastAPI backend, conversation persistence, and response handling.

### Web interface

- Browser-based chat interface.
- Question submission and answer display.
- Session-aware conversation support.
- Configurable webhook endpoint.
- Nginx hosting in a container.

### Observability

- API and RAG processing logs.
- Logging of relevant processing and model activity.
- n8n execution records and conversation data.
- Information to support troubleshooting of failed requests.

Logging provides useful diagnostic information, but it is not a substitute for a dedicated monitoring or alerting platform.

## Knowledge base and answer policy

The assistant is designed to answer questions using retrieved document passages as its primary evidence. Conversation history helps interpret follow-up questions, while document retrieval supplies supporting context.

When the available documents do not contain a sufficient answer, the model is instructed to respond:

> I don't know based on the provided documents.

This instruction encourages grounded responses but cannot guarantee that every generated answer is accurate or free from unsupported claims.

## Project structure

```text
rag-assistant/
├── api/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   ├── assets/
│   │   └── favicon.ico
│   ├── app.js
│   ├── config.js
│   ├── index.html
│   └── style.css
├── ingestion/
│   ├── __init__.py
│   ├── build_vector_db.py
│   ├── ingest.py
│   └── pdf_loader.py
├── n8n/
│   └── workflows/
│       └── AI Research Assistant - RAG v1.0.json
├── rag/
│   ├── __init__.py
│   ├── engine.py
│   ├── llm.py
│   ├── retriever.py
│   ├── startup.py
│   └── state.py
├── screenshots/
│   └── AI_Research_Assistant.mp4
├── tests/
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_chroma.py
│   │   ├── test_ollama.py
│   │   └── test_rag_pipeline.py
│   └── unit/
│       ├── __init__.py
│       ├── test_config.py
│       └── test_retriever_logic.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── config.py
├── logging_config.py
├── pytest.ini
├── README.md
└── requirements.txt
```

The repository excludes the local document collection, generated vector database, environment secrets, logs, caches, and archived snapshots. These resources are managed separately from the version-controlled application code.

## Requirements

- Linux or another operating system supported by Docker.
- Docker Engine.
- Docker Compose.
- Ollama installed and running on the host.
- A compatible Ollama model downloaded locally.
- Python 3.12 or later for local ingestion tasks.
- Sufficient memory and processing capacity for the selected embedding and language models.

The model and hardware requirements depend on the configured models and workload.

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd rag-assistant
```

Replace `<repository-url>` with the repository's Git URL.

### 2. Configure environment variables

Create a local environment file from the example:

```bash
cp .env.example .env
```

Review `.env` and adjust the values for the local environment. Keep `.env` private and do not commit it.

The example configuration covers the following settings:

| Variable | Purpose |
|---|---|
| `OLLAMA_HOST` | Address used by the API to reach Ollama |
| `LLM_MODEL` | Ollama model used to generate answers |
| `EMBEDDING_MODEL` | Sentence Transformers embedding model |
| `SEARCH_K` | Number of candidate results considered during retrieval |
| `TOP_K` | Number of relevant results selected for context |
| `MAX_DISTANCE` | Retrieval distance threshold |
| `CHUNK_SIZE` | Target document chunk size |
| `CHUNK_OVERLAP` | Overlap between consecutive chunks |
| `API_PORT` | Host port for the FastAPI service |
| `N8N_PORT` | Host port for the n8n service |
| `FRONTEND_PORT` | Host port for the frontend |

The defaults are defined in `.env.example`. The application configuration and Compose file determine which values are consumed by each component.

The provided Ollama host setting should be appropriate for a container accessing Ollama on the host. If Ollama runs in a different location, configure the address accordingly.

### 3. Prepare Ollama

Start Ollama and download the model configured in `.env`.

For example, to download the default model if it is set to `gemma3:4b`:

```bash
ollama pull gemma3:4b
```

If a different model is configured, download that model instead. Ensure the configured model is available to the running Ollama service before testing question answering.

### 4. Prepare the knowledge base

The API expects an existing ChromaDB collection. If a prepared vector database is not available, create it from the source documents before starting the application.

Create a Python virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then, from the repository root, run the ingestion entry point:

```bash
python -m ingestion.build_vector_db
```

**Important:** This script rebuilds the vector database collection. Run it intentionally when creating or updating the knowledge base, not for each question. Back up any data that needs to be preserved before rebuilding.

The ingestion process must be able to access the configured source documents and download or load the required embedding model.

### 5. Start the services

From the repository root, start the containers:

```bash
docker-compose up -d
```

Check their status:

```bash
docker-compose ps
```

Inspect service logs when troubleshooting:

```bash
docker-compose logs --tail=100
```

To inspect a specific service, use its Compose service name, for example:

```bash
docker-compose logs --tail=100 rag-api
docker-compose logs --tail=100 n8n
docker-compose logs --tail=100 frontend
```

The API, n8n workflow, Ollama service, and existing vector database must be configured consistently for the full request lifecycle to work.

## Local endpoints

With the default port configuration:

| Service | URL |
|---|---|
| Web interface | [http://localhost:8080](http://localhost:8080) |
| n8n editor | [http://localhost:5678](http://localhost:5678) |
| FastAPI | [http://localhost:8000](http://localhost:8000) |
| FastAPI Swagger UI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| FastAPI ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| API health check | [http://localhost:8000/health](http://localhost:8000/health) |

The actual host ports are determined by the Compose configuration and environment variables.

## API usage

### Check API health

```bash
curl http://localhost:8000/health
```

Use the response to confirm that the health endpoint is reachable. A successful health check does not necessarily prove that Ollama, the embedding model, or the vector database is ready to answer questions.

### Submit a question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is an n8n webhook?",
    "history": []
  }'
```

The request includes a question and an optional conversation history. The response contains the generated answer and may include source information, according to the API response schema.

The interactive API documentation at `/docs` provides the current request and response schemas.

## Testing

The project includes unit and integration tests using `pytest`.

### Unit tests

Unit tests check required configuration values and basic context formatting.

### Integration tests

Integration tests exercise ChromaDB retrieval, the Ollama language-model integration, and the RAG pipeline. They require the relevant local services, configuration, and knowledge base to be available.

### Run the tests

Install the project dependencies in a Python virtual environment as described in the setup instructions, then run the tests from the repository root.

Run unit tests:

```bash
pytest tests/unit/
```

Run integration tests:

```bash
pytest tests/integration/
```

Run the complete test suite:

```bash
pytest
```

The integration tests may require a populated ChromaDB collection and a running Ollama service with the configured model available. Results depend on the local environment.

The current suite provides basic configuration checks and integration smoke tests. It does not constitute comprehensive coverage of document ingestion, API behavior, n8n workflow execution, retrieval quality, or answer accuracy.

## Configuration and operation

The primary configuration files are:

- `.env.example` — template for local environment settings.
- `.env` — local configuration, excluded from version control.
- `config.py` — application settings and default values.
- `docker-compose.yml` — service definitions, networking, volumes, ports, and environment variables.
- `frontend/config.js` — frontend webhook configuration.

When changing model names, retrieval settings, service addresses, or ports, review the relevant configuration files together.

### Persistent data

The vector database is stored in the configured `vector_db/` location and mounted into the API container. The n8n service uses persistent storage for its application data.

Keep backups of any data that must survive a rebuild, reinstall, or host failure. Do not assume that deleting and recreating a container also deletes its persistent volumes, or that rebuilding a vector database preserves its previous contents.

### Security and privacy

The application is designed for local use. Local inference and storage can reduce dependence on external AI services, but they do not automatically guarantee complete privacy or security.

- Keep `.env` and credentials out of version control.
- Avoid placing confidential information in public logs or workflow execution records.
- Protect access to the n8n editor and API if the application is exposed beyond the local machine.
- Review the handling and retention of conversation history and source documents.
- Secure any remote Ollama, API, or database endpoints appropriately.

## Current limitations

- Answer quality depends on the source documents, retrieval relevance, and selected language model.
- Inference speed and resource consumption depend on the hardware and model size.
- Authentication and role-based access control are not implemented as application features.
- Knowledge-base updates require an intentional ingestion and rebuild operation.
- Automated retrieval and answer-quality evaluation is not implemented.
- A dedicated monitoring dashboard and production alerting system are not included.
- Local deployment does not by itself provide high availability, production-grade security, or disaster recovery.

## Potential improvements

- Add authentication and access controls.
- Introduce automated retrieval and answer-quality evaluation.
- Add document connectors and controlled update workflows.
- Add human review for uncertain or sensitive answers.
- Improve operational monitoring and alerting.
- Expand automated test coverage for document ingestion, API endpoints, and n8n workflow behavior.
- Add continuous integration (CI) checks to run automated tests consistently.
- Improve deployment automation and recovery procedures.

## Development note

This is a personal portfolio project exploring local AI application architecture, retrieval-augmented generation, API integration, workflow automation, and containerized services.

AI-assisted development tools were used during implementation and learning. The project is intended to demonstrate the architecture, implementation, and troubleshooting process rather than claim a production deployment.

## License

No open-source license is currently specified. Unless a license is added to the repository, no permission to reuse, modify, or distribute this project should be assumed.
