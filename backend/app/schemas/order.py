from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional


class OrderStatus(str, Enum):
    processing = "в обработке"
    canceled = "отменен"
    completed = "выполнен"

class OrderBase(BaseModel):
    client_id: int
    photographer_id: str
    date_requested: str
    type: str
    location: str
    status: OrderStatus
    deadline: str
    final_price: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    client_id: Optional[int] = None
    photographer_id: Optional[str] = None
    date_requested: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[OrderStatus] = None
    deadline: Optional[str] = None
    final_price: Optional[str] = None

class OrderInDB(OrderBase):
    id: int = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
