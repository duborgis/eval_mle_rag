from abc import ABC, abstractmethod


class LLM(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def generate_response(self, question: str, context: str) -> str:
        pass

    @abstractmethod
    def create_prompt(self, question: str, context: str) -> str:
        pass
