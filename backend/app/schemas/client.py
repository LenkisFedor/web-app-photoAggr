# app/schemas/client.py
from pydantic import BaseModel, Field
from typing import List, Optional

class HistoryItem(BaseModel):
    photographer_id: int
    date: str
    type: str

class ClientBase(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    preferences: List[str]
    history: Optional[List[HistoryItem]] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None
    history: Optional[List[HistoryItem]] = None

class ClientInDB(ClientBase):
    id: int = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
