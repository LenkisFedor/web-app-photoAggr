from pydantic import BaseModel, Field
from typing import List

class Request(BaseModel):
    id: int = Field(alias="_id")
    date_requested: str
    type: str
    location: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
