from pydantic import BaseModel, Field
from typing import List, Optional


class RequestBase(BaseModel):
    client_id: int
    date_requested: str
    type: str
    location: str

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    client_id: Optional[int] = None
    date_requested: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None

class RequestInDB(RequestBase):
    id: int = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
