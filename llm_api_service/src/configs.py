import os

HS256_PASSWORD = os.getenv("HS256_PASSWORD", "exemploHotmart")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:1b")
VECTOR_SERVICE_HOST = os.getenv("VECTOR_SERVICE_HOST", "localhost")
VECTOR_SERVICE_PORT = os.getenv("VECTOR_SERVICE_PORT", "5002")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
VERSION = "0.0.1"
LOG_LEVEL = "INFO"
VECTOR_SERVICE_URL = (
    f"http://{VECTOR_SERVICE_HOST}:{VECTOR_SERVICE_PORT}/vector/vectorize-ask"
)
