from typing import Optional

from pydantic import BaseModel, HttpUrl

class ResearchResult(BaseModel):
    """
    Çıkan sonucu, kullanılan kaynak linklerini ve güven skorunu tutacak model.
    """

    result_text : str
    source : Optional[HttpUrl] = None
    confidence_score : float



