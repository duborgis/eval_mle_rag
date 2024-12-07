from abc import ABC, abstractmethod


class AbstractEmbeddingModel(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def create_embeddings(self, question: str) -> str:
        pass

    @abstractmethod
    def create_embeddings_batch(self, texts: list[str]):
        pass
