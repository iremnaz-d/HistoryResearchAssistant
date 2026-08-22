from pydantic import BaseModel
from typing import Optional


class Query(BaseModel):
    """
    A simple model representing the user's question.
    """

    raw_query: str
    research_question : Optional[str] = None
    language : Optional[str] = None