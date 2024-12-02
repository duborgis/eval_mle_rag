import os

HS256_PASSWORD = os.getenv('HS256_PASSWORD', 'exemploHotmart')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2:1b')
VERSION = "0.0.1"
LOG_LEVEL = "INFO"
VECTOR_SERVICE_URL = "http://load_vector_service:5002/vector/vectorize-ask"
