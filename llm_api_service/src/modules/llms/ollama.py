from .abstract_class import LLM
import ollama


class Ollama(LLM):
    def __init__(self, model_name: str, host: str, port: int):
        super().__init__(model_name)
        self.host = host
        self.port = port
        self.client = None
        self.load_model()

    def load_model(self) -> None:
        self.client = ollama.Client(f"{self.host}:{self.port}")
        self.client.pull(model=self.model_name)

    def create_prompt(self, question: str, context_text: str) -> str:
        prompt = f"""Baseado no contexto abaixo, responda a pergunta de forma clara e concisa. Mas traga as informações mais relevantes.
            Se a resposta não puder ser encontrada no contexto, diga "Não tenho informações suficientes para responder."

            Contexto:
            {context_text}

            Pergunta: {question}

            Resposta:"""

        return prompt

    def generate_response(self, prompt: str) -> str:
        response: ollama.ChatResponse = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response.message.content
