from src.domain.entities.document import Document
from src.domain.entities.research_query import Query
from src.domain.entities.research_result import ResearchResult


class ContextBuilder:
    """
    This class takes a ResearchResult object and returns the complete prompt and context to be sent to the LLM
    """

    @staticmethod
    def build_web(query:Query, search_results : list[ResearchResult]):
        with open("src/application/prompts/context_build_web.txt", "r", encoding = "utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(
            user_query = query.raw_query,
            language = query.language,
            research_result = ResearchResult.list_to_text(search_results)
        )

        return prompt

    @staticmethod
    def build_rag(query:Query, results:list[list[ResearchResult]], documents : list[Document]):
        result_list = [i for sublist in results for i in sublist]

        with open("src/application/prompts/context_build_rag.txt", "r", encoding = "utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(
            user_query = query.raw_query,
            language = query.language,
            results = ResearchResult.list_to_text(result_list),
            documents = Document.list_to_text(documents)
        )

        return prompt

