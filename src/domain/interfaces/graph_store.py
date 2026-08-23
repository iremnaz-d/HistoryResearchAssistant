from abc import ABC, abstractmethod

class GraphStoreInterface(ABC):

    @abstractmethod
    def add_entity(self, entity):
        pass

    @abstractmethod
    def add_relation(self, source, target, relation_type, evidence_url):
        pass

    @abstractmethod
    def query_graph(self, entity):
        pass

