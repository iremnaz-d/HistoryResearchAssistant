from pydantic import BaseModel

class Concept(BaseModel):
    id : str
    name : str