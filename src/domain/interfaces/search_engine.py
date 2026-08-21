from abc import ABC, abstractmethod

from src.domain.entities.research_query import Query


class SearchEngineInterface(ABC):
    """
    "Web'de arama yapacak sınıfın mutlaka bir search fonksiyonu olmalıdır" kuralını tanımlayan şablon.
    """

    @abstractmethod
    def search(self, query: Query):
        pass


