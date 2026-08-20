from pydantic import BaseModel, HttpUrl

class Result(BaseModel):
    """
    Çıkan sonucu, kullanılan kaynak linklerini ve güven skorunu tutacak model.
    """

    result_text : str
    sources : list[HttpUrl]
    confidence_score : float

