from .abstract_class import AbstractEmbeddingModel
from .utils import check_gpu_available
from langchain_community.embeddings import HuggingFaceEmbeddings


class StAllMiniEmbeddingModel(AbstractEmbeddingModel):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = self.load_model()
        self.vector_size = 384

    def load_model(self):
        device = "cuda" if check_gpu_available() else "cpu"
        print(f"Using device: {device}")

        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        model_kwargs = {"device": device}
        encode_kwargs = {"normalize_embeddings": True}

        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

        return embeddings

    def create_embeddings(self, question: str):
        embedding = self.model.embed_query(question)
        return embedding

    def create_embeddings_batch(self, chunks: list[str], batch_size: int):
        embeddings = []
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i : i + batch_size]

            batch_embeddings = self.model.embed_documents(batch_chunks)
            embeddings.append(batch_embeddings)

        return embeddings[0]
