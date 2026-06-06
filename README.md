# Code Understanding RAG

A production-ready RAG (Retrieval-Augmented Generation) system for code understanding, analysis, and documentation generation.

## Features

- **Code Parsing & Analysis**: Parse code files, extract AST, functions, classes, imports, docstrings
- **RAG System**: Code embeddings, semantic search, context retrieval, similarity analysis
- **Documentation**: Auto-generate README, function/class docs, architecture docs, API docs
- **Q&A System**: Explain code, answer questions, compare patterns, suggest alternatives
- **Code Review**: Quality assessment, style checking, best practices, security/performance issues
- **Visualization**: Code structure diagrams, dependency graphs, call graphs, architecture diagrams

## Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd code-understanding-rag

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run the backend
uvicorn backend.main:app --reload

# Run the frontend
cd frontend && npm install && npm start
```

## Tech Stack

- **Backend**: FastAPI, Python
- **Code Parsing**: AST (Abstract Syntax Tree)
- **RAG**: LangChain
- **Embeddings**: OpenAI, HuggingFace
- **LLM**: GPT-4, Claude, Groq
- **Vector DB**: Chroma, FAISS, Pinecone
- **Frontend**: React, Redux
- **Database**: PostgreSQL
- **Cache**: Redis
- **Testing**: Pytest
- **Deployment**: Docker
- **Monitoring**: Prometheus, Grafana

## Project Structure

```
code-understanding-rag/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── notebooks/         # Jupyter notebooks
├── examples/          # Usage examples
├── tests/             # Test suite
├── scripts/           # Utility scripts
├── data/              # Data files
├── docs/              # Documentation
├── config/            # Configuration
└── monitoring/        # Monitoring config
```

## License

MIT
