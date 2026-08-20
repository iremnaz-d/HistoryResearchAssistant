from abc import ABC, abstractmethod


class LLMClientInterface(ABC):
    """
    "LLM ile konuşacak sınıfın mutlaka bir generate fonksiyonu olmalıdır" kuralını tanımlayan şablon.
    """

    @abstractmethod
    def generate(self):
        pass

