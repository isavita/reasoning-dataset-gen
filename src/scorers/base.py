from abc import ABC, abstractmethod

class BaseScorer(ABC):
    def __init__(self, model_name: str = None, temperature: float = 0.3):
        self.model_name = model_name
        self.temperature = temperature

    @abstractmethod
    def score(self, user_prompt: str, assistant_response: str) -> int:
        """Score the given text"""
        pass
