from typing import Optional
from pydantic import BaseModel, HttpUrl

class ResearchResult(BaseModel):
    """
    This model stores the search_engines result from the search_engines engine, the source used, and the confidence score
    """

    result_text : str
    source : Optional[HttpUrl] = None
    confidence_score : float

    @staticmethod
    def list_to_text(results: list["ResearchResult"]):
        s = ""
        for result in results:
            s += str(result.source)
            s += "\n" + result.result_text + "\n\n"

        return s
