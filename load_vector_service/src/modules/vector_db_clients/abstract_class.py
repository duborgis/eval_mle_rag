from abc import ABC, abstractmethod


class VectorDBClientAbstractClass(ABC):
    def __init__(self, vector_client_name: str):
        self.vector_client_name = vector_client_name

    @abstractmethod
    def create_collection(self, collection_name: str, vector_size: int, distance: str):
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def query_vector(self, question: str, collection_name: str):
        pass

    @abstractmethod
    def insert_points_collection(self, collection_name: str, points: list):
        pass
