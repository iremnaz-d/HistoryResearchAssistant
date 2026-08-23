from abc import ABC, abstractmethod

class MemoryStoreInterface(ABC):

    @abstractmethod
    def save_knowledge(self):
        pass

    @abstractmethod
    def search_knowledge(self):
        pass