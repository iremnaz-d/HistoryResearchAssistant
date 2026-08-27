from src.application.rag.indexing_service import GraphIndexingService, VectorIndexingService
from src.application.rag.retrieval_service import GraphRetrievalService, VectorRetrievalService
from src.application.research.research_service import ResearchService
from src.domain.entities.research_query import Query
from src.domain.interfaces.embedding_model import EmbeddingModelInterface
from src.domain.interfaces.graph_store import GraphStoreInterface
from src.domain.interfaces.llm_client import LLMClientInterface
from src.domain.interfaces.search_engine import SearchEngineInterface
from src.domain.interfaces.vector_store import VectorStoreInterface


class MainResearchService:

    def __init__(self, search_engine: SearchEngineInterface, llm_client: LLMClientInterface,
                 embedding_model : EmbeddingModelInterface, graph_db: GraphStoreInterface,
                 vector_db : VectorStoreInterface):

        self.search_engine = search_engine
        self.llm_client = llm_client
        self.embedding_model = embedding_model
        self.graph_db = graph_db
        self.vector_db = vector_db

        self.graph_indexing_service = GraphIndexingService(graph_store = self.graph_db)
        self.vector_indexing_service = VectorIndexingService(vector_db = self.vector_db)

        self.research_service = ResearchService(
            search_engine = self.search_engine,
            llm_client = self.llm_client,
            embedding_model = self.embedding_model,
            graph_db = self.graph_db,
            vector_db  =  self.vector_db
        )

    def get_answer(self, query: Query, chat_history):

        rag_answer = self.research_service.get_research_answer_rag(
            raw_query = query.raw_query,
            chat_history = chat_history
        )

        if not rag_answer:
            web_answer, results= self.research_service.get_research_answer_web(
                raw_query = query.raw_query,
                chat_history = chat_history
            )

            self.graph_indexing_service.save(results = results)
            self.vector_indexing_service.save(results = results)

            return web_answer

        else:
            return rag_answer
