# Importar o client
from qdrant_client import QdrantClient

# Criar nossa coleção
from qdrant_client.http.models import Distance, VectorParams


from qdrant_client.http import models
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import uuid
from pynvml import nvmlInit, nvmlDeviceGetCount, NVMLError

qdrant_client = QdrantClient("localhost", port=6333)


def check_gpu_available():
    try:
        nvmlInit()
        n_gpus = nvmlDeviceGetCount()
        return n_gpus > 0
    except NVMLError:
        return False


def load_model_on_init():
    device = "cuda" if check_gpu_available() else "cpu"
    print(f"Using device: {device}")

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    return embeddings


embeddings_model = load_model_on_init()


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
                # Split chunks grandes usando pontuação
                sub_splitter = CharacterTextSplitter(
                    separator=".", chunk_size=200, chunk_overlap=50, length_function=len
                )
                sub_chunks = sub_splitter.split_text(chunk)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)

        # Limpa e normaliza os chunks
        cleaned_chunks = [
            chunk.strip()
            for chunk in final_chunks
            if len(chunk.strip()) > 50  # Remove chunks muito pequenos
        ]

        return cleaned_chunks
    except Exception as e:
        print(f"Erro ao dividir texto: {str(e)}")
        return []


client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="test_collection_2",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

with open("./utils/out/output.txt", "r") as f:
    texts = f.read()

chunks = get_chunks(texts)

print(f"Total de chunks: {len(chunks)}")

batch_size = 50

for i in range(0, len(chunks), batch_size):
    batch_texts = chunks[i : i + batch_size]

    batch_embeddings = embeddings_model.embed_documents(batch_texts)

    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
        )
        for idx, embedding in enumerate(batch_embeddings)
    ]

    operation_info = qdrant_client.upsert(
        collection_name="test_collection_2", points=points, wait=True
    )
