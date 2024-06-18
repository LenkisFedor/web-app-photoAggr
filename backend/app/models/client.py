from pydantic import BaseModel, Field
from typing import List, Optional

class HistoryItem(BaseModel):
    photographer_id: int
    date: str
    type: str

class Client(BaseModel):
    id: int = Field(alias="_id")
    name: str
    email: str
    phone: str
    location: str
    preferences: List[str]
    history: Optional[List[HistoryItem]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True