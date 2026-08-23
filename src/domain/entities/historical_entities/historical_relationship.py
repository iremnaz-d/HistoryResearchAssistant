from pydantic import BaseModel, HttpUrl

class Relationship(BaseModel):
    source_id : str
    target_id : str
    type : str
    evidence_url: HttpUrl | None = None