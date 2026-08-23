from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    id: str
    name: str
    start_date : datetime | None = None
    end_date : datetime | None = None
    description : str | None = None
