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

    def get_research_answer(self, raw_query, chat_history):

        query = self.create_processed_query(raw_query, chat_history)
        search_results = self.search_engine.search(query)
        context = ContextBuilder.build(query, search_results)
        llm_response = self.llm_client.generate(context, history = chat_history)
        return llm_response.text

    def create_processed_query(self, raw_query, chat_history):
        query, language = self.translate_to_english(raw_query)
        reformulated_query = self.reformulate_query(query, chat_history)
        research_query = f"A detailed historical and academic article about: {reformulated_query}"
        return Query(raw_query = query, research_question = research_query, language = language)



    @staticmethod
    def translate_to_english(text):
        detected_lang = detect(text)
        if detected_lang == "en":
            return text, "en"

        translator = GoogleTranslator(source='auto', target="en")

        translated_text = translator.translate(text)
        return translated_text, detected_lang

    def reformulate_query(self, query:str, chat_history: list[str]):
        if not chat_history:
            return query

        with open("src/application/prompts/reformulate_query.txt","r",encoding="utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(
            chat_history = str(chat_history),
            user_query = query
        )
        new_query = self.llm_client.generate(prompt)
        return new_query.text




