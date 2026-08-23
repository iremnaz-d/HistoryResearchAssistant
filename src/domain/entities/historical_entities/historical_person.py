from pydantic import BaseModel
from datetime import datetime

class Person(BaseModel):
    name : str
    id : str
    birth_date : datetime | None = None
    death_date: datetime | None = None