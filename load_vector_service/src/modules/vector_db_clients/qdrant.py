from .abstract_class import VectorDBClientAbstractClass
from qdrant_client import QdrantClient
from qdrant_client import models
import uuid
import sys
import os


class QdrantClientClass(VectorDBClientAbstractClass):
    def __init__(self, url: str, port: int):
        super().__init__("qdrant")
        self.url = url
        self.port = port
        self.client = QdrantClient(url=self.url, port=self.port)

    def create_collection(
        self, collection_name: str, vector_size: int = 384, distance: str = "cosine"
    ):
        try:
            collections = self.client.get_collections().collections
            collection_exists = any(col.name == collection_name for col in collections)

            if collection_exists:
                print(f"Collection {collection_name} already exists")
                raise Exception(f"Collection {collection_name} already exists")

            if distance == "cosine":
                distance = models.Distance.COSINE
            elif distance == "euclidean":
                distance = models.Distance.EUCLID

            response = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=distance,
                ),
            )
            print(response)
            return True
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False

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
        try:
            points = [
                models.PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload)
                for vector, payload in zip(vectors, payloads)
            ]
            print(collection_name)
            operation_info = self.client.upsert(
                collection_name=collection_name, points=points, wait=True
            )
            return operation_info
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
