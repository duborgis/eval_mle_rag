import vecs
from .abstract_class import VectorDBClientAbstractClass
from src.configs import SUPABASE_URL, SUPABASE_PROJECT_REF, SUPABASE_KEY


class SupabaseClientClass(VectorDBClientAbstractClass):
    def __init__(self, url: str, port: int):
        super().__init__("supabase")
        self.url = url
        self.port = port
        self.client = vecs.Client(url=self.url, port=self.port)
        self.db_connection = vecs.create_client(
            connection_string=f"postgresql://{SUPABASE_KEY}@{SUPABASE_URL}/{SUPABASE_PROJECT_REF}"
        )

    def create_collection(
        self, collection_name: str, vector_size: int = 384, distance: str = "cosine"
    ):
        self.client.create_collection(collection_name, vector_size, distance)

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(collection_name)

    def query_vector(self, embedding: list, collection_name: str):
        self.db_connection.query(embedding, collection_name)

    def insert_points_collection(self, collection_name: str, points: list):
        self.db_connection.upsert(collection_name, points)
