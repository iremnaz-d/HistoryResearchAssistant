from src.application.rag.context_builder import ContextBuilder
from src.domain.entities.research_query import Query
from src.domain.interfaces.llm_client import LLMClientInterface
from src.domain.interfaces.search_engine import SearchEngineInterface
from deep_translator import GoogleTranslator
from langdetect import detect

class ResearchService:

    def __init__(self, search_engine: SearchEngineInterface, llm_client: LLMClientInterface):
        self.search_engine = search_engine
        self.llm_client = llm_client

    def get_research_answer(self, raw_query):

        query = self.create_processed_query(raw_query)
        search_results = self.search_engine.search(query)
        context = ContextBuilder.build(query, search_results)
        llm_response = self.llm_client.generate(context)
        return llm_response.text

    def create_processed_query(self, raw_query):
        query, language = self.translate_to_english(raw_query)
        return Query(raw_query = query, research_question = query, language = language) # raw_query = research_question because of Exa



    @staticmethod
    def translate_to_english(text):
        detected_lang = detect(text)
        if detected_lang == "en":
            return text, "en"

        translator = GoogleTranslator(source='auto', target="en")

        translated_text = translator.translate(text)
        return translated_text, detected_lang
