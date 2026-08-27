from src.application.graph.entity_extractor import EntityExtractor
from src.domain.interfaces.graph_store import GraphStoreInterface
from src.domain.interfaces.vector_store import VectorStoreInterface
from src.infrastructure.llm_clients.groq_client import GroqClient

class GraphRetrievalService:

    def __init__(self, graph_db: GraphStoreInterface):
        self.graph_db = graph_db
        llm_client = GroqClient()
        self.entity_extractor = EntityExtractor(llm_client)

    def retrieve(self, query: str):
        entity_list, relation_list = self.entity_extractor.extract(query = query)
        results = []

        for entity in entity_list:
            result_list = self.graph_db.query_graph(entity)
            results.append(result_list)

        return results #iç içe result list


class VectorRetrievalService:

    def __init__(self, vector_db : VectorStoreInterface):
        self.vector_db = vector_db

    def retrieve(self, query:str):
        document_list = self.vector_db.search(query = query)
        return document_list