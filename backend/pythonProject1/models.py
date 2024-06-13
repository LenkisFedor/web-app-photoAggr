from pydantic import BaseModel, Field
from typing import List, Optional

class Request(BaseModel):
    client_id: int
    date_requested: str
    type: str
    location: str


class Employee(BaseModel):
    id: int  # Это поле добавлено для модели Employee для работы с PostgreSQL
    name: str
    role: str
    email: str
    phone: str
    department: str


class Service(BaseModel):
    name: str
    description: str
    price: float


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


class Photographer(BaseModel):
    name: str
    email: str
    phone: str
    location: str


class Order(BaseModel):
    service_id: int
    client_id: int
    photographer_id: int
    order_date: str
    status: str