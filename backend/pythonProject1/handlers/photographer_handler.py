from fastapi import APIRouter, HTTPException
from bson import ObjectId   
from models import Photographer
from db import photographers_collection

router = APIRouter()

@router.get("/photographers", response_model=list[Photographer])
def get_photographers():
    photographers = list(photographers_collection.find())
    for photographer in photographers:
        photographer['_id'] = str(photographer['_id'])
    return photographers

@router.get("/photographers/{photographer_id}", response_model=Photographer)
def get_photographer(photographer_id: str):
    photographer = photographers_collection.find_one({"_id": ObjectId(photographer_id)})
    if photographer:
        photographer['_id'] = str(photographer['_id'])
        return photographer
    else:
        raise HTTPException(status_code=404, detail="Photographer not found")

@router.post("/photographers/", response_model=dict)
def create_photographer(photographer: Photographer):
    photographer_data = photographer.dict()
    photographer_id = photographers_collection.insert_one(photographer_data).inserted_id
    return {"message": "Photographer created successfully", "photographer_id": str(photographer_id)}

@router.put("/photographers/{photographer_id}", response_model=dict)
def update_photographer(photographer_id: str, photographer: Photographer):
    photographer_data = photographer.dict()
    result = photographers_collection.update_one({"_id": ObjectId(photographer_id)}, {"$set": photographer_data})
    if result.modified_count == 1:
        return {"message": "Photographer updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Photographer not found")

@router.delete("/photographers/{photographer_id}", response_model=dict)
def delete_photographer(photographer_id: str):
    result = photographers_collection.delete_one({"_id": ObjectId(photographer_id)})
    if result.deleted_count == 1:
        return {"message": "Photographer deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Photographer not found")
