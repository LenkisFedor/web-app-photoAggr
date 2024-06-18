from pydantic import BaseModel, Field
from typing import List, Optional


class ServiceBase(BaseModel):
    service_type: str
    description: str
    price: int


class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    service_type: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None


class ServiceInDB(ServiceBase):
    id: int = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
