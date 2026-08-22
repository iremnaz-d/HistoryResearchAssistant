from pydantic import BaseModel
from typing import Optional


class Query(BaseModel):
    """
    Kullanıcının sorusunu temsil eden basit model.
    """

    raw_query: str
    research_question : Optional[str] = None
    language : Optional[str] = None