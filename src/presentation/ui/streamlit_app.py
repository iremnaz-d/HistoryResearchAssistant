import sys
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

from src.infrastructure.llm_clients.groq_client import GroqClient
from src.application.research.main_research_flow import MainResearchService
from src.infrastructure.embeddings.BGE_M3_embedding_model import BgeEmbedding
from src.infrastructure.persistance.ChromaDB_vector_store import ChromaDB
from src.infrastructure.persistance.KuzuDB_graph_store import KuzuDB
import streamlit as st
from src.infrastructure.llm_clients.gemini_client import GeminiClient
from src.infrastructure.search_engines.exa_search import ExaSearchEngine
from google.genai.errors import ServerError, ClientError



def main():
    search_engine = ExaSearchEngine()
    llm_client_1 = GeminiClient()
    llm_client_2 = GeminiClient() #bunun groq olması gerekiyo da error verdi
    embedding_model = BgeEmbedding()
    graph_db = KuzuDB()
    vector_db = ChromaDB(embedding_model = embedding_model)

    research_service = MainResearchService(
        search_engine = search_engine,
        llm_client_1 = llm_client_1,
        llm_client_2 = llm_client_2,
        graph_db = graph_db,
        vector_db = vector_db
    )


    # rendering chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])


    if raw_query := st.chat_input("Ask something"):
        st.session_state.messages.append({'role': 'user', 'content': raw_query})
        with st.chat_message('user'):
            st.markdown(raw_query)

        try:
            response = research_service.get_answer(raw_query = raw_query, chat_history = st.session_state.messages)
            st.session_state.messages.append({'role': 'model', 'content': response})
            with st.chat_message('model'):
                st.markdown(response)

        except ServerError:
            error_message = "AI Assistant is not available at this moment. Please try again a few minutes later."
            st.session_state.messages.append({'role': 'model', 'content': error_message})
            with st.chat_message('model'):
                st.markdown(error_message)

        except ClientError as e:
            error_str = str(e).lower()
            if "429" in error_str:
                if 'minute' in error_str:
                    error_message = "You hit the speed limit per minute. Please try again 1 minute later."
                elif 'day' in error_str or 'daily' in error_str:
                    error_message = "You have reached daily AI Assistant chat limit. Please try again tomorrow."
                else:
                    error_message = "Too many request! This Assistant is tired. Please wait a while and try again later."

            else:
                error_message = "Unexpected client error. Did you enter your API Key?"
            st.session_state.messages.append({'role': 'model', 'content': error_message})
            with st.chat_message('model'):
                st.markdown(error_message)

main()