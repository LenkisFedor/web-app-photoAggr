from pydantic import BaseModel, Field
from typing import List, Optional


class PhotographerBase(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    specialization: List[str]
    experience: int

class PhotographerCreate(PhotographerBase):
    pass

class PhotographerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    specialization: Optional[List[str]] = None
    experience: Optional[int] = None

class PhotographerInDB(PhotographerBase):
    id: int = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
