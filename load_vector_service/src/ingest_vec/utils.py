from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import sys
import os
import uuid
from pynvml import nvmlInit, nvmlDeviceGetCount, NVMLError
import hashlib
qdrant_client = QdrantClient("localhost", port=6333)

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
                # Split chunks grandes usando pontuação
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
        
        # Limpa e normaliza os chunks
        cleaned_chunks = [
            chunk.strip()
            for chunk in final_chunks
            if len(chunk.strip()) > 50  # Remove chunks muito pequenos
        ]
        
        return cleaned_chunks
    except Exception as e:
        print(f"Erro ao dividir texto: {str(e)}")
        return []


def normalize_name_collection(collection_name: str):
    # cria um hash do nome da collection
    return hashlib.md5(collection_name.encode()).hexdigest()


def check_collection_exists(collection_name: str):
    collection_name = normalize_name_collection(collection_name)
    collections = qdrant_client.get_collections().collections
    collection_exists = any(col.name == collection_name for col in collections)
    return collection_exists


def vectorize_ask_function(question: str, collection_name: str):
    try:
        collection_name = normalize_name_collection(collection_name)
        embedding = embeddings_model.embed_query(question)
        search_result = qdrant_client.search(
            collection_name=collection_name, 
            query_vector=embedding, 
            limit=3,
            score_threshold=0.5
        )
        print(search_result)
        contexts = []
        for result in search_result:
            print(result.payload, hasattr(result.payload, 'text'))
            if 'text' in result.payload:
                contexts.append(result.payload['text'])
        
        context_text = "\n".join(contexts)
        return context_text
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)

def create_and_store_embeddings(
    texts: str,
    metadata_list: List[Dict[str, Any]],
    collection_name: str,
    batch_size: int = 50
) -> None:
    try:
        collection_name = normalize_name_collection(collection_name)
        collections = qdrant_client.get_collections().collections
        collection_exists = any(col.name == collection_name for col in collections)
        
        if not collection_exists:
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Dimensão do modelo all-MiniLM-L6-v2
                    distance=models.Distance.COSINE
                )
            )
        
        chunks = get_chunks(texts)

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
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)


def delete_collection(collection_name: str):
    collection_name = normalize_name_collection(collection_name)
    qdrant_client.delete_collection(collection_name)
