import os
from src.application.agent.router import Router
from src.application.rag.context_builder import ContextBuilder
from src.application.rag.retrieval_service import GraphRetrievalService, VectorRetrievalService
from src.domain.entities.research_query import Query
from src.domain.interfaces.graph_store import GraphStoreInterface
from src.domain.interfaces.llm_client import LLMClientInterface
from src.domain.interfaces.search_engine import SearchEngineInterface
from deep_translator import GoogleTranslator
from langdetect import detect
from src.domain.interfaces.vector_store import VectorStoreInterface


class ResearchService:

    def __init__(self, search_engine: SearchEngineInterface, llm_client_1: LLMClientInterface,
                 llm_client_2 :LLMClientInterface,
                 graph_db: GraphStoreInterface,vector_db : VectorStoreInterface):

        self.current_dir = os.path.dirname(__file__)

        self.search_engine = search_engine
        self.llm_client_1 = llm_client_1
        self.llm_client_2 = llm_client_2
        self.graph_db = graph_db
        self.vector_db = vector_db

        self.graph_retrieval_service = GraphRetrievalService(graph_db  =self.graph_db)
        self.vector_retrieval_service = VectorRetrievalService(vector_db = self.vector_db)

    def get_research_answer_web(self, raw_query, chat_history):

        query , reformulated_query = self.create_processed_query(raw_query, chat_history) # gets 'Query' object from raw_query
        search_results = self.search_engine.search(query) # gets web search_engines results from Search Engine
        context = ContextBuilder.build_web(query, search_results) # gets the context to send the main LLM
        llm_response = self.llm_client_1.generate(context, history = chat_history) #gets the final answer from LLM
        return llm_response.text, search_results

    def get_research_answer_rag(self, raw_query, chat_history):
        query, reformulated_query = self.create_processed_query(raw_query, chat_history)  # gets 'Query' object from raw_query

        graph_results = self.graph_retrieval_service.retrieve(query = query.raw_query)
        vector_results = self.vector_retrieval_service.retrieve(query = query.raw_query)

        router = Router(llm_client = self.llm_client_2)
        sufficient = router.is_sufficient(query = reformulated_query, graph_results = graph_results, vector_results = vector_results)

        if not sufficient:
            return False

        else:
            context = ContextBuilder.build_rag(query=query, results=graph_results, documents=vector_results)
            llm_response = self.llm_client_1.generate(context, history=chat_history)
            return llm_response.text

    def create_processed_query(self, raw_query, chat_history):
        """
        This method translates the user's query into English and saves the original language.
        It converts it to the appropriate format for the Search Engine and creates the Query object.

        :param raw_query: First form of the user question (string)
        :param chat_history: chat history (list)
        :return: 'Query' Object
        """
        query, language = self.translate_to_english(raw_query)
        reformulated_query = self.reformulate_query(query, chat_history)
        research_query = f"A detailed historical and academic article about: {reformulated_query}"
        return Query(raw_query = query, research_question = research_query, language = language), reformulated_query

    def reformulate_query(self, query:str, chat_history: list[str]):
        """
        This method is designed specifically for follow-up questions.
        It sends the conversation history and the user’s new question to the LLM,
        converting them into a question format that Exa can process.

        :param query: translated query (string)
        :param chat_history: chat history (list)
        :return: new question (string)
        """
        if not chat_history:
            return query

        prompt_path = os.path.join(self.current_dir,"..", "prompts","reformulate_query.txt")

        with open(prompt_path, "r", encoding="utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(
            chat_history = str(chat_history),
            user_query = query
        )
        new_query = self.llm_client_2.generate(text = prompt)
        return new_query.text

    @staticmethod
    def translate_to_english(text):
        detected_lang = detect(text)
        if detected_lang == "en":
            return text, "en"

        translator = GoogleTranslator(source='auto', target="en")

        translated_text = translator.translate(text)
        return translated_text, detected_lang