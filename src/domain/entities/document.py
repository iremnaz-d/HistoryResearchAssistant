from pydantic import BaseModel, HttpUrl

class Document(BaseModel):
    id : str
    text : str
    source : HttpUrl | None = None
    