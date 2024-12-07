import os

HS256_PASSWORD = os.getenv("HS256_PASSWORD", "exemploHotmart")
VERSION = "0.0.1"
LOG_LEVEL = "INFO"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
