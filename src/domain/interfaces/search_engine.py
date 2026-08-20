from abc import ABC, abstractmethod


class SearchEngineInterface(ABC):
    """
    "Web'de arama yapacak sınıfın mutlaka bir search fonksiyonu olmalıdır" kuralını tanımlayan şablon.
    """

    @abstractmethod
    def search(self):
        pass


