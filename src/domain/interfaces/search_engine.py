from abc import ABC, abstractmethod

from src.domain.entities.research_query import Query


class SearchEngineInterface(ABC):

    @abstractmethod
    def search(self, query: Query):
        pass


