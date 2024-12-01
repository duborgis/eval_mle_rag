import os

HS256_PASSWORD = os.getenv('HS256_PASSWORD', 'exemploHotmart')
VERSION = "0.0.1"
LOG_LEVEL = "INFO"
VECTOR_SERVICE_URL = "http://load_vector_service:5002/vector/vectorize-ask"
