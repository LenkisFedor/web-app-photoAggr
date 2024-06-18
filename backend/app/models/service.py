from pydantic import BaseModel, Field
from typing import List, Optional

class Service(BaseModel):
    id: int = Field(alias="_id")
    service_type: str
    description: str
    price: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True