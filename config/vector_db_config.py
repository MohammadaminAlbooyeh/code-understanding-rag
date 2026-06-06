VECTOR_DB_CONFIG = {
    "chroma": {
        "persist_directory": "./data/vector_db",
        "collection_name": "code_embeddings",
    },
    "faiss": {
        "dimension": 1536,
        "index_path": "./data/vector_db/faiss.index",
    },
    "pinecone": {
        "environment": "us-west1-gcp",
        "index_name": "code-embeddings",
        "dimension": 1536,
        "metric": "cosine",
    },
}
