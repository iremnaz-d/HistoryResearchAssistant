from src.application.graph.entity_extractor import EntityExtractor
from src.domain.entities.research_result import ResearchResult
from src.domain.interfaces.graph_store import GraphStoreInterface
from src.infrastructure.llm_clients.groq_client import GroqClient

class GraphIndexingService:

    def __init__(self, graph_store: GraphStoreInterface):
        self.graph_store = graph_store
        llm_client = GroqClient()
        self.extractor = EntityExtractor(llm_client)

    def save(self, results: list[ResearchResult]):

        entity_list, relation_list = self.extractor.extract(results)

        entity_lookup = {}
        for entity in entity_list:
            self.graph_store.add_entity(entity)
            entity_lookup[entity.id] = entity

        for relation in relation_list:
            source = entity_lookup.get(relation.source.id)
            target = entity_lookup.get(relation.target.id)

            if source and target:
                self.graph_store.add_relation(
                    source = source,
                    target = target,
                    relation_type = relation.type,
                    evidence_url=relation.evidence_url
                )
            else:
                raise ValueError("Source or Target is not found in GraphIndexingService")