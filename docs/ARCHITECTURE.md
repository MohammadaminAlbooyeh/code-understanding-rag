# Architecture

## System Overview

The system consists of:
- **Backend**: FastAPI application with modular code analysis, RAG, and service layers
- **Frontend**: React SPA with Redux state management
- **Vector Store**: Chroma/FAISS/Pinecone for embedding storage
- **Database**: PostgreSQL for metadata and results
- **Cache**: Redis for performance

## Layers

1. **API Layer** - REST endpoints
2. **Service Layer** - Business logic
3. **Code Analysis Layer** - Parsing and analysis
4. **RAG Layer** - Embeddings, retrieval, LLM chains
5. **Storage Layer** - Vector DB, PostgreSQL, Redis
