from fastapi import APIRouter, HTTPException
from typing import List
from schemas.photographer import PhotographerCreate, PhotographerUpdate, PhotographerInDB  # Assuming you have schemas for photographer in schemas.photographer
from crud.photographer import get_photographers, get_photographer, create_photographer, update_photographer, delete_photographer  # Importing functions from crud.photographer

router = APIRouter()

@router.get("/", response_model=List[PhotographerInDB])
async def read_photographers():
    return await get_photographers()

@router.get("/{photographer_id}", response_model=PhotographerInDB)
async def read_photographer(photographer_id: int):
    photographer = await get_photographer(photographer_id)
    if photographer:
        return photographer
    raise HTTPException(status_code=404, detail="Photographer not found")

@router.post("/", response_model=PhotographerInDB)
async def add_photographer(photographer: PhotographerCreate):
    return await create_photographer(photographer)

@router.put("/{photographer_id}", response_model=PhotographerInDB)
async def modify_photographer(photographer_id: int, photographer: PhotographerUpdate):
    updated_photographer = await update_photographer(photographer_id, photographer)
    if updated_photographer:
        return updated_photographer
    raise HTTPException(status_code=404, detail="Photographer not found")

@router.delete("/{photographer_id}", response_model=dict)
async def remove_photographer(photographer_id: int):
    result = await delete_photographer(photographer_id)
    if result:
        return {"message": "Photographer successfully deleted"}
    raise HTTPException(status_code=404, detail="Photographer not found")
