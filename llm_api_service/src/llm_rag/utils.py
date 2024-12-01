
import hashlib
from qdrant_client import QdrantClient
import requests
import httpx
from ..configs import VECTOR_SERVICE_URL
from ollama import chat, pull
from ollama import ChatResponse

qdrant_client = QdrantClient("localhost", port=6333)


def load_model_on_init():
    pull(model='llama3.2:1b')

def normalize_name_collection(collection_name: str):
    return hashlib.md5(collection_name.encode()).hexdigest()


def create_prompt(question: str, context_text: str) -> str:

    prompt = f"""Baseado no contexto abaixo, responda a pergunta de forma clara e concisa. Mas traga as informações mais relevantes.
    Se a resposta não puder ser encontrada no contexto, diga "Não tenho informações suficientes para responder."

    Contexto:
    {context_text}

    Pergunta: {question}
    
    Resposta:"""
    
    return prompt


async def get_vector_search_results(question: str, collection_name: str) -> str:
    """Faz requisição ao serviço de vetorização"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                VECTOR_SERVICE_URL,
                data={
                    "question": question,
                    "collection_name": collection_name
                },
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.json().get("detail", "")
        
    except requests.RequestException as e:
        print(f"Erro na requisição ao serviço de vetorização: {str(e)}")
        raise Exception("Falha ao obter resultados da busca vetorial")


async def generate_response(question: str, collection_name: str) -> str:
    search_results = await get_vector_search_results(question, collection_name)
    prompt = create_prompt(question, search_results)
    print(prompt)
    response: ChatResponse = chat(model='llama3.2:1b', messages=[
    {
            "role": "user",
            "content": prompt,
        },
    ])
    print(response.message.content)
    return response.message.content




