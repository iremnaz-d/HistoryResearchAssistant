import os
from exa_py import Exa

from src.config.settings import Settings
from src.domain.entities.research_query import Query
from src.domain.entities.research_result import ResearchResult
from src.domain.interfaces.search_engine import SearchEngineInterface


class ExaSearchEngine(SearchEngineInterface):

    def __init__(self):
        self.settings = Settings()
        self.exa = Exa(self.settings.exa_api_key)


    def search(self, query: Query):

        try:
           raw_response =  self.exa.search(
                query=query.research_question,
                num_results = self.settings.MAX_SEARCH_RESULTS,
                contents={"text":True}, # type:ignore
            )
           return self.map_to_result(raw_response)

        except Exception as e:
            return ResearchResult(
                result_text = f"There has been an error during web research: {str(e)}",
                source = None, confidence_score = 0.0
            )


    @staticmethod
    def map_to_result(raw_response):
        """
        :param raw_response: raw search result taken from Exa API
        :return: "Result" Object List
        """
        if not raw_response.results:
            return ResearchResult(result_text = "No results found.", source=None, confidence_score = 0.0)

        results = []

        for result in raw_response.results:
            text = None
            score = None

            if hasattr(result, "text") and result.text:
                text = result.text

            if hasattr(result, "score") and result.score:
                score = result.score

            results.append(ResearchResult(result_text = text, source = result.url, confidence_score = score))

        return results
