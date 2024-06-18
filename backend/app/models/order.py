from pydantic import BaseModel, Field
from typing import List

class Order(BaseModel):
    id: int = Field(alias="_id")
    client_id: int
    photographer_id: str
    date_requested: str
    type: str
    location: str
    status: str
    deadline: str
    final_price: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
