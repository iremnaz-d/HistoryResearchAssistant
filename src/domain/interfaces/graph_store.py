from abc import ABC, abstractmethod

class GraphStoreInterface(ABC):

    @abstractmethod
    def add_node(self, entity):
        pass

    @abstractmethod
    def add_edge(self, source, target, relation_type):
        pass

    @abstractmethod
    def get_relations(self, entity_id):
        pass

