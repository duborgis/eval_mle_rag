from pynvml import nvmlInit, nvmlDeviceGetCount, NVMLError
import hashlib
from nltk.corpus import stopwords
import nltk
from langchain.text_splitter import CharacterTextSplitter
from src.modules.vector_db_clients import QdrantClientClass
from src.modules.embeddings import OLLamaEmbeddingModel
import sys
import os

nltk.download("stopwords")

qdrant_client = QdrantClientClass(url="localhost", port=6333)
embeddings_model = OLLamaEmbeddingModel("test_model", host="localhost", port=11434)


def retrieve_similar_data(question: str, collection_name: str):
    try:
        collection_name = normalize_name_collection(collection_name)
        embedding = embeddings_model.create_embeddings(question)
        context_text = qdrant_client.query_vector(embedding, collection_name)
        return context_text
    except Exception as e:
        print(f"Erro ao buscar dados similares: {str(e)}")
        return ""


def create_and_store_embeddings(
    texts: str, collection_name: str, batch_size: int = 50
) -> None:
    try:
        collection_name = normalize_name_collection(collection_name)
        qdrant_client.create_collection(
            collection_name, embeddings_model.vector_size, "cosine"
        )
        chunks = get_chunks(texts)  # Dividir o texto em chunks
        print(len(chunks))
        batch_embeddings = embeddings_model.create_embeddings_batch(chunks, batch_size)
        batch_payloads = [{"text": text} for text in chunks]
        qdrant_client.insert_points_collection(
            collection_name, batch_embeddings, batch_payloads
        )
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def check_gpu_available():
    try:
        nvmlInit()
        n_gpus = nvmlDeviceGetCount()
        return n_gpus > 0
    except NVMLError:
        return False


def get_chunks(text: str):
    try:
        text_splitter = CharacterTextSplitter(
            separator=".",
            chunk_size=300,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )

        # Primeiro split por parágrafos
        chunks = text_splitter.split_text(text)

        final_chunks = []
        max_chunk_size = 300

        for chunk in chunks:
            if len(chunk) > max_chunk_size:
                sub_splitter = CharacterTextSplitter(
                    separator=".", chunk_size=200, chunk_overlap=50, length_function=len
                )
                sub_chunks = sub_splitter.split_text(chunk)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)

        cleaned_chunks = [normalize_chunk(chunk) for chunk in final_chunks]

        return cleaned_chunks
    except Exception as e:
        print(f"Erro ao dividir texto: {str(e)}")
        return []


def normalize_chunk(text: str):
    text = text.strip()

    text = text.lower()

    stop_words = set(stopwords.words("portuguese"))
    text = " ".join([word for word in text.split() if word not in stop_words])

    return text


def normalize_name_collection(collection_name: str):
    # cria um hash do nome da collection
    return hashlib.md5(collection_name.encode()).hexdigest()
