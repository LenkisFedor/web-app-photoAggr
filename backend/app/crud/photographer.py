from fastapi import HTTPException
from db import photographers_collection
from models.photographer import Photographer
from schemas.photographer import PhotographerInDB, PhotographerCreate, PhotographerUpdate
from utils.sequences import get_next_sequence_value
from typing import List

async def get_photographers() -> List[PhotographerInDB]:
    photographers = photographers_collection.find()
    return [PhotographerInDB(**photographer) for photographer in photographers]

async def get_photographer(photographer_id: int) -> PhotographerInDB:
    photographer = photographers_collection.find_one({"_id": photographer_id})
    if photographer:
        return PhotographerInDB(**photographer)
    raise HTTPException(status_code=404, detail="Photographer not found")

async def create_photographer(photographer_data: PhotographerCreate) -> PhotographerInDB:
    photographer_id = get_next_sequence_value("photographers")
    photographer_dict = photographer_data.dict()
    photographer_dict["_id"] = photographer_id
    photographers_collection.insert_one(photographer_dict)
    return PhotographerInDB(**photographer_dict)

async def update_photographer(photographer_id: int, photographer_data: PhotographerUpdate) -> PhotographerInDB:
    existing_photographer = photographers_collection.find_one({"_id": photographer_id})
    if existing_photographer:
        updated_photographer_data = photographer_data.dict(exclude_unset=True)
        updated_photographer = {**existing_photographer, **updated_photographer_data}
        photographers_collection.update_one({"_id": photographer_id}, {"$set": updated_photographer})
        return PhotographerInDB(**updated_photographer)
    raise HTTPException(status_code=404, detail="Photographer not found")

async def delete_photographer(photographer_id: int):
    result = photographers_collection.delete_one({"_id": photographer_id})
    if result.deleted_count == 1:
        return {"message": "Photographer deleted successfully"}
    raise HTTPException(status_code=404, detail="Photographer not found")
