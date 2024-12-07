import requests
import httpx
import asyncio

from ollama import chat, pull
from ollama import ChatResponse

VECTOR_SERVICE_URL = "http://localhost:5002/vector/vectorize-ask"


pull(model="llama3.2:1b")


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
                data={"question": question, "collection_name": collection_name},
                timeout=30.0,
            )

            response.raise_for_status()
            return response.json().get("detail", "")

    except requests.RequestException as e:
        print(f"Erro na requisição ao serviço de vetorização: {str(e)}")
        raise Exception("Falha ao obter resultados da busca vetorial")


async def generate_response(question: str, collection_name: str) -> str:
    search_results = await get_vector_search_results(question, collection_name)
    prompt = create_prompt(question, search_results)
    response: ChatResponse = chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.message.content


if __name__ == "__main__":
    print(
        asyncio.run(
            generate_response(
                "O que faz a Hotmart?",
                "O que é Hotmart e como funciona? DESCUBRA TUDO!",
            )
        )
    )
