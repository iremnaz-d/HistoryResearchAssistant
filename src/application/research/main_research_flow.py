from src.application.rag.indexing_service import GraphIndexingService, VectorIndexingService
from src.application.research.research_service import ResearchService
from src.domain.interfaces.graph_store import GraphStoreInterface
from src.domain.interfaces.llm_client import LLMClientInterface
from src.domain.interfaces.search_engine import SearchEngineInterface
from src.domain.interfaces.vector_store import VectorStoreInterface


class MainResearchService:

    def __init__(self, search_engine: SearchEngineInterface, llm_client_1: LLMClientInterface,
                 llm_client_2: LLMClientInterface,
                graph_db: GraphStoreInterface, vector_db : VectorStoreInterface):

        self.search_engine = search_engine
        self.llm_client_1 = llm_client_1
        self.llm_client_2 = llm_client_2
        self.graph_db = graph_db
        self.vector_db = vector_db

        self.graph_indexing_service = GraphIndexingService(graph_store = self.graph_db)
        self.vector_indexing_service = VectorIndexingService(vector_db = self.vector_db)

        self.research_service = ResearchService(
            search_engine = self.search_engine,
            llm_client_1 = self.llm_client_1,
            llm_client_2 = self.llm_client_2,
            graph_db = self.graph_db,
            vector_db  =  self.vector_db
        )

    def get_answer(self, raw_query, chat_history):

        rag_answer = self.research_service.get_research_answer_rag(
            raw_query = raw_query,
            chat_history = chat_history
        )

        if not rag_answer:
            web_answer, results= self.research_service.get_research_answer_web(
                raw_query = raw_query,
                chat_history = chat_history
            )

            self.graph_indexing_service.save(results = results)
            self.vector_indexing_service.save(results = results)

            return web_answer

        else:
            return rag_answer
