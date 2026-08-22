import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)


import streamlit as st
from src.application.research.research_service import ResearchService
from src.infrastructure.llm.gemini_client import GeminiClient
from src.infrastructure.search.exa_search import ExaSearchEngine
from google.genai.errors import ServerError, ClientError



def main():
    search_engine = ExaSearchEngine()
    llm_client = GeminiClient()
    research_service = ResearchService(search_engine, llm_client)


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
            response = research_service.get_research_answer(raw_query)
            st.session_state.messages.append({'role': 'assistant', 'content': response})
            with st.chat_message('assistant'):
                st.markdown(response)

        except ServerError:
            error_message = "AI Assistant is not available at this moment. Please try again a few minutes later."
            st.session_state.messages.append({'role': 'assistant', 'content': error_message})
            with st.chat_message('assistant'):
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
            st.session_state.messages.append({'role': 'assistant', 'content': error_message})
            with st.chat_message('assistant'):
                st.markdown(error_message)

main()