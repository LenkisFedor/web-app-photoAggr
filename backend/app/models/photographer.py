from pydantic import BaseModel, Field
from typing import List

class Photographer(BaseModel):
    id: int = Field(alias="_id")
    name: str
    email: str
    phone: str
    location: str
    specialization: List[str]
    experience: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
