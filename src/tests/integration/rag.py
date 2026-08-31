import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

from src.application.research.main_research_flow import MainResearchService
from src.infrastructure.embeddings.BGE_M3_embedding_model import BgeEmbedding
from src.infrastructure.llm_clients.gemini_client import GeminiClient
from src.infrastructure.persistance.ChromaDB_vector_store import ChromaDB
from src.infrastructure.persistance.KuzuDB_graph_store import KuzuDB
from src.infrastructure.search_engines.exa_search import ExaSearchEngine


def test_main_research_flow():

    search_engine = ExaSearchEngine()
    llm_client_1 = GeminiClient()
    llm_client_2 = GeminiClient()  # bunun groq olması gerekiyo da error verdi
    embedding_model = BgeEmbedding()
    graph_db = KuzuDB()
    vector_db = ChromaDB(embedding_model=embedding_model)

    research_service = MainResearchService(
        search_engine=search_engine,
        llm_client_1=llm_client_1,
        llm_client_2=llm_client_2,
        graph_db=graph_db,
        vector_db=vector_db
    )

    raw_query = "Hitler hangi ülkede doğmuştur?"
    chat_history = []

    answer = research_service.get_answer(raw_query = raw_query, chat_history = chat_history)
    print(answer)

if __name__ == '__main__':
    test_main_research_flow()

