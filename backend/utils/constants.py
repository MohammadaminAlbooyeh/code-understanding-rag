SUPPORTED_LANGUAGES = [
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "cpp",
    "rust",
]

ANALYSIS_TYPES = [
    "parse",
    "complexity",
    "bugs",
    "security",
    "patterns",
    "dependencies",
    "flow",
]

DOCUMENTATION_TYPES = [
    "function",
    "class",
    "module",
    "api",
    "readme",
]

VECTOR_STORE_TYPES = ["chroma", "faiss", "pinecone"]

LLM_PROVIDERS = ["openai", "anthropic", "groq"]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.7
