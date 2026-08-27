from src.application.graph.entity_extractor import EntityExtractor
from src.domain.entities.document import Document
from src.domain.entities.research_result import ResearchResult
from src.domain.interfaces.graph_store import GraphStoreInterface
from src.domain.interfaces.vector_store import VectorStoreInterface
from src.infrastructure.llm_clients.gemini_client import GeminiClient
from src.infrastructure.llm_clients.groq_client import GroqClient
import hashlib

class GraphIndexingService:

    def __init__(self, graph_store: GraphStoreInterface):
        self.graph_store = graph_store
        llm_client = GeminiClient()  #burası da groq client normalde
        self.extractor = EntityExtractor(llm_client)

    def save(self, results: list[ResearchResult]):

        entity_list, relation_list = self.extractor.extract(results = results)

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

class VectorIndexingService:

    def __init__(self, vector_db : VectorStoreInterface):
        self.vector_db = vector_db

    def save(self, results:list[ResearchResult]):
        documents = []
        for result in results:
            document_id = hashlib.sha256(result.result_text.encode("utf-8")).hexdigest()
            documents.append(Document(id = document_id, text = result.result_text, source = result.source))

        self.vector_db.add_documents(documents)

