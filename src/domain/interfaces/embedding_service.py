from abc import ABC, abstractmethod

class EmbeddingModelInterface(ABC):

    @abstractmethod
    def embed(self, text: str):
        pass

