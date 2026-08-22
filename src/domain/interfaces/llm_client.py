from abc import ABC, abstractmethod


class LLMClientInterface(ABC):

    @abstractmethod
    def generate(self, text, tools = None, history = None):
        pass

