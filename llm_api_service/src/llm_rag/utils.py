import hashlib
import requests
import httpx
from ..configs import VECTOR_SERVICE_URL, MODEL_NAME
from ollama import ChatResponse
from ollama import Client

client = Client(
    host="http://ollama:11434",
)


def load_model_on_init():
    client.pull(model=MODEL_NAME)


load_model_on_init()


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
            response = (
                await client.post(  # Content-Type: application/x-www-form-urlencoded
                    VECTOR_SERVICE_URL,
                    data={"question": question, "collection_name": collection_name},
                    timeout=30.0,
                )
            )

            response.raise_for_status()
            return response.json().get("detail", "")

    except requests.RequestException as e:
        print(f"Erro na requisição ao serviço de vetorização: {str(e)}")
        raise Exception("Falha ao obter resultados da busca vetorial")


async def generate_response(question: str, collection_name: str) -> str:
    try:
        search_results = await get_vector_search_results(question, collection_name)
        prompt = create_prompt(question, search_results)
        print(prompt)
        response: ChatResponse = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return {
            "response": response.message.content,
            "rag_search_results": search_results,
        }
    except Exception as e:
        print(f"Erro ao gerar resposta: {str(e)}")
        raise Exception("Não tenho informações suficientes para responder.")
