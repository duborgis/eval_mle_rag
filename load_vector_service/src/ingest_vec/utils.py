from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import uuid
from pynvml import nvmlInit, nvmlDeviceGetCount, NVMLError
import hashlib
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')



qdrant_client = QdrantClient("qdrant", port=6333)

def check_gpu_available():
    try:
        nvmlInit()
        n_gpus = nvmlDeviceGetCount()
        return n_gpus > 0
    except NVMLError:
        return False

def load_model_on_init():

    device = 'cuda' if check_gpu_available() else 'cpu'
    print(f"Using device: {device}")
    
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': True}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    return embeddings

embeddings_model = load_model_on_init()


def get_chunks(text: str):
    try:
        text_splitter = CharacterTextSplitter(
            separator=".",  
            chunk_size=300,  
            chunk_overlap=50,  
            length_function=len,
            is_separator_regex=False
        )
        
        # Primeiro split por parágrafos
        chunks = text_splitter.split_text(text)
        
        final_chunks = []
        max_chunk_size = 300
        
        for chunk in chunks:
            if len(chunk) > max_chunk_size:
                sub_splitter = CharacterTextSplitter(
                    separator=".",
                    chunk_size=200,
                    chunk_overlap=50,
                    length_function=len
                )
                sub_chunks = sub_splitter.split_text(chunk)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)
        
        cleaned_chunks = [
            normalize_chunk(chunk)
            for chunk in final_chunks
        ]
        
        return cleaned_chunks
    except Exception as e:
        print(f"Erro ao dividir texto: {str(e)}")
        return []


def normalize_chunk(text: str):
    text = text.strip()

    text = re.sub(r'[^\w\s]', '', text)

    text = text.lower()

    text = re.sub(r'[^a-zA-Z\s]', '', text)

    stop_words = set(stopwords.words('portuguese'))
    text = ' '.join([word for word in text.split() if word not in stop_words])

    return text

def retrieve_similar_data(question: str, collection_name: str):
    collection_name = normalize_name_collection(collection_name)
    embedding = embeddings_model.embed_query(question)
    search_result = qdrant_client.search(
        collection_name=collection_name, 
        query_vector=embedding, 
        limit=5,
        score_threshold=0.5
    )
    contexts = []
    for result in search_result:
        if 'text' in result.payload:
            contexts.append(result.payload['text'])
    
    context_text = "\n".join(contexts)
    return context_text


def create_and_store_embeddings(
    texts: str,
    collection_name: str,
    batch_size: int = 50
) -> None:
    collection_name = normalize_name_collection(collection_name)
    collections = qdrant_client.get_collections().collections
    collection_exists = any(col.name == collection_name for col in collections)
    
    if collection_exists:
        print(f"Collection {collection_name} already exists")
        raise Exception(f"Collection {collection_name} already exists")

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384,  # Dimensão do modelo all-MiniLM-L6-v2
            distance=models.Distance.COSINE
        )
    )

    chunks = get_chunks(texts) # Dividir o texto em chunks

    for i in range(0, len(chunks), batch_size):
        batch_texts = chunks[i:i + batch_size]
        
        batch_embeddings = embeddings_model.embed_documents(batch_texts)
        
        points = [
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"text": text}
            )
            for embedding, text in zip(batch_embeddings, batch_texts)
        ]

        operation_info = qdrant_client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True
        )

        print(operation_info)
        
        print(f"Processed and stored batch {i//batch_size + 1} of {(len(texts)-1)//batch_size + 1}")


def normalize_name_collection(collection_name: str):
    # cria um hash do nome da collection
    return hashlib.md5(collection_name.encode()).hexdigest()