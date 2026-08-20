from pydantic import BaseModel
from typing import Optional


class Query(BaseModel):
    """
    Kullanıcının sorusunu temsil eden basit model.
    """

    original_query: str
    research_question : Optional[str] = None



