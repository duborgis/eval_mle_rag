from .abstract_class import VectorDBClientAbstractClass
from qdrant_client import QdrantClient
from qdrant_client import models
import uuid


class QdrantClientClass(VectorDBClientAbstractClass):
    def __init__(self, url: str):
        super().__init__("qdrant")
        self.url = url
        self.client = QdrantClient(url=self.url)

    def create_collection(
        self, collection_name: str, vector_size: int = 384, distance: str = "cosine"
    ):
        collections = self.client.get_collections().collections
        collection_exists = any(col.name == collection_name for col in collections)

        if collection_exists:
            print(f"Collection {collection_name} already exists")
            raise Exception(f"Collection {collection_name} already exists")

        if distance == "cosine":
            distance = models.Distance.COSINE
        elif distance == "euclidean":
            distance = models.Distance.EUCLID

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=distance,
            ),
        )
        return True

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(collection_name)
        return True

    def query_vector(self, embedding: list, collection_name: str):
        search_result = self.client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=5,
            score_threshold=0.5,
        )
        contexts = []
        for result in search_result:
            if "text" in result.payload:
                contexts.append(result.payload["text"])

        context_text = "\n".join(contexts)
        return context_text

    def insert_points_collection(
        self, collection_name: str, vectors: list, payloads: list
    ):
        points = [
            models.PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload)
            for vector, payload in zip(vectors, payloads)
        ]
        operation_info = self.client.upsert(
            collection_name=collection_name, points=points, wait=True
        )
        return operation_info
