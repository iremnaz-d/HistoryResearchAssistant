from abc import ABC, abstractmethod

from src.domain.entities.document import Document


class VectorStoreInterface(ABC):

    @abstractmethod
    def add_documents(self, documents:list[Document]):
        pass

    @abstractmethod
    def search(self, query : str):
        pass
