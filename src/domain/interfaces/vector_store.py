from abc import ABC, abstractmethod

class VectorStoreInterface(ABC):

    @abstractmethod
    def add_documents(self, texts, metadata):
        pass

    @abstractmethod
    def similarity_search(self, query_vector):
        pass
