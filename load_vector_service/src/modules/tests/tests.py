from ..vector_db_clients import QdrantClientClass
from ..embeddings import StAllMiniEmbeddingModel
from .mocks import vectors, payloads, question, chunks

qdrant_client = QdrantClientClass(url="http://localhost:6333")


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


embedding_model = StAllMiniEmbeddingModel("test_model")


def test_create_embeddings():
    embedding = embedding_model.create_embeddings(question)
    print("embedding", embedding)
    assert len(embedding) == 384


def test_create_embeddings_batch():
    embeddings = embedding_model.create_embeddings_batch(chunks)
    print("embeddings", embeddings)
    assert len(embeddings) == len(chunks)
