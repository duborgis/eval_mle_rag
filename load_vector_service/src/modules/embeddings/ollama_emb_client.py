from .abstract_class import AbstractEmbeddingModel
import ollama


class OLLamaEmbeddingModel(AbstractEmbeddingModel):
    def __init__(self, model_name: str, host: str = "ollama", port: int = 11434):
        super().__init__(model_name)
        self.model = self.load_model(host, port)
        self.vector_size = 768

    def load_model(self, host: str, port: int):
        client = ollama.Client(f"http://{host}:{port}")
        client.pull("nomic-embed-text")
        return client

    def create_embeddings(self, document: str):
        embedding = self.model.embeddings(model="nomic-embed-text", prompt=document)
        return embedding.embedding

    def create_embeddings_batch(self, chunks: list[str], batch_size: int):
        embeddings = []
        for i, d in enumerate(chunks):
            embedding = self.create_embeddings(d)
            embeddings.append(embedding)
        return embeddings
