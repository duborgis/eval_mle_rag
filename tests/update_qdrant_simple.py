# Importar o client
from qdrant_client import QdrantClient

# Criar nossa coleção
from qdrant_client.http.models import Distance, VectorParams

# Criar nossos vetores
from qdrant_client.http.models import PointStruct

# Pretty Printer
from pprint import pprint

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)


operation_info = client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"continente": "Europa", "cidade": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"continente": "Europa", "cidade": "Londres"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"continente": "America", "cidade": "Nova York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"continente": "Asia", "cidade": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"continente": "Asia", "cidade": "Mumbai"}),
    ],
)

pprint(operation_info)