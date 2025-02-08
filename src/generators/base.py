from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response for the given prompt"""
        pass

    @staticmethod
    @abstractmethod
    def get_system_prompt() -> str:
        """Return the system prompt for this generator"""
        pass
