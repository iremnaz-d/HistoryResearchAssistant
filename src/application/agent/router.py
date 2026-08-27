from src.domain.entities.document import Document
from src.domain.entities.research_result import ResearchResult
from src.domain.interfaces.llm_client import LLMClientInterface


class Router:
    def __init__(self, llm_client: LLMClientInterface):
        self.llm_client = llm_client


    def is_sufficient(self,query: str, graph_results: list[list[ResearchResult]], vector_results: list[Document] ):
        graph_result_list = [i for sublist in graph_results for i in sublist]
        graph_text = ResearchResult.list_to_text(results = graph_result_list)
        vector_text = Document.list_to_text(documents = vector_results)

        with open("src/application/prompts/router.txt", "r", encoding = "utf-8") as f:
            raw_prompt = f.read()

        prompt = raw_prompt.format(
            user_query = query,
            graph_results = graph_text,
            vector_results = vector_text,
        )
        response = self.llm_client.generate(text = prompt)
        if response == "True":
            return True
        elif response == "False":
            return False
        else:
            raise ValueError("Router could not return a value True/False")