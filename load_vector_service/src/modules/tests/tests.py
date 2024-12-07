from ..vector_db_clients import QdrantClientClass
from ..embeddings import OLLamaEmbeddingModel
from .mocks import vectors, payloads, question, chunks, documents
from langchain.text_splitter import CharacterTextSplitter
import hashlib
# from nltk.corpus import stopwords


qdrant_client = QdrantClientClass(url="localhost", port=6333)


# ---------------- tests vector db client ----------------


def test_create_collection():
    qdrant_client.delete_collection("test_collection")
    assert qdrant_client.create_collection("test_collection", 4, "cosine")


def test_insert_points_collection():
    assert qdrant_client.insert_points_collection(
        "test_collection",
        vectors,
        payloads,
    )


def test_query_vector():
    question_vector = [0.05, 0.61, 0.76, 0.74]
    result = qdrant_client.query_vector(question_vector, "test_collection")
    print("result", result)
    assert True


# ---------------- tests embeddings ----------------


# embedding_model = StAllMiniEmbeddingModel("test_model")


# def test_create_embeddings():
#     embedding = embedding_model.create_embeddings(question)
#     assert len(embedding) == 384


# def test_create_embeddings_batch():
#     embeddings = embedding_model.create_embeddings_batch(chunks, len(chunks))
#     print("embeddings", embeddings)
#     assert len(embeddings) == len(chunks)


ollama_embedding_model = OLLamaEmbeddingModel(
    "test_model", host="localhost", port=11434
)


# def test_ollama_create_embeddings_batch():
#     embeddings = ollama_embedding_model.create_embeddings_batch(
#         documents, len(documents)
#     )
#     print("embeddings", embeddings)
#     assert len(embeddings) == len(documents)


def test_complete_process():
    qdrant_client.delete_collection("test_collection")

    print("vector_size", ollama_embedding_model.vector_size)

    qdrant_client.create_collection(
        "test_collection", ollama_embedding_model.vector_size, "cosine"
    )

    with open("output.txt", "r") as file:
        text = file.read()

    chunks_texts = get_chunks(text)

    print("chunks_texts", chunks_texts[0])

    embeddings = ollama_embedding_model.create_embeddings_batch(
        chunks_texts, len(chunks_texts)
    )

    assert ollama_embedding_model.vector_size == len(embeddings[0])

    print("embeddings", embeddings[0], len(embeddings[0]), type(embeddings[0]))

    assert len(embeddings) == len(chunks_texts)

    payloads = [{"text": chunk} for chunk in chunks_texts]
    qdrant_client.insert_points_collection("test_collection", embeddings, payloads)

    assert True


# ---------------- utils ----------------


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

    # stop_words = set(stopwords.words("portuguese"))
    # text = " ".join([word for word in text.split() if word not in stop_words])

    return text


def normalize_name_collection(collection_name: str):
    # cria um hash do nome da collection
    return hashlib.md5(collection_name.encode()).hexdigest()
