import hashlib
import requests
import httpx
from ..configs import VECTOR_SERVICE_URL, MODEL_NAME, OLLAMA_HOST, OLLAMA_PORT
from ..modules.llms import Ollama

ollama = Ollama(model_name=MODEL_NAME, host=OLLAMA_HOST, port=OLLAMA_PORT)


def normalize_name_collection(collection_name: str):
    return hashlib.md5(collection_name.encode()).hexdigest()


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
        prompt = ollama.create_prompt(question, search_results)
        response = ollama.generate_response(prompt)
        return {
            "response": response,
            "rag_search_results": search_results,
        }
    except Exception as e:
        print(f"Erro ao gerar resposta: {str(e)}")
        raise Exception("Não tenho informações suficientes para responder.")
