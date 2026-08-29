from pydantic import BaseModel
from datetime import date

class Person(BaseModel):
    name : str
    id : str
    birth_date : date | None = None
    death_date: date | None = None