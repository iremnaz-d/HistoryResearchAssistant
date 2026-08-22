from src.domain.entities.research_query import Query
from src.domain.entities.research_result import ResearchResult


class ContextBuilder:
    """
    This class takes a ResearchResult object and returns the complete prompt and context to be sent to the LLM
    """

    @staticmethod
    def build(query:Query, search_results : list[ResearchResult]):
        with open("src/application/prompts/context_build.txt", "r", encoding = "utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(
            user_query = query.raw_query,
            language = query.language,
            sources = ResearchResult.list_to_text(search_results)
        )

        return prompt

