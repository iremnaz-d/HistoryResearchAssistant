from src.domain.entities.research_result import ResearchResult
from src.domain.interfaces.llm_client import LLMClientInterface


class EntityExtractor:

    def __init__(self, llm_client: LLMClientInterface):
        self.llm_client = llm_client

    def extract(self, results : list[ResearchResult]):
        full_result = ResearchResult.list_to_text(results) #web search results from search engine

        with open("src/application/prompts/entity_extract.txt", "r", encoding = "utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(provided_sources = full_result)

        structured_json_output = self.llm_client.generate(text = prompt)



