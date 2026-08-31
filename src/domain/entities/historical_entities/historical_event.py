from pydantic import BaseModel
from datetime import date


class Event(BaseModel):
    id: str
    name: str
    start_date : date | None = None
    end_date : date | None = None
    description : str | None = None
