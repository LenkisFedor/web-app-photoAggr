from fastapi import APIRouter, HTTPException
from typing import List
from schemas.request import RequestCreate, RequestUpdate, RequestInDB  # Assuming you have schemas for request in schemas.request
from crud.request import get_requests, get_request, create_request, update_request, delete_request  # Importing functions from crud.request

router = APIRouter()

@router.get("/", response_model=List[RequestInDB])
async def read_requests():
    return await get_requests()

@router.get("/{request_id}", response_model=RequestInDB)
async def read_request(request_id: int):
    request = await get_request(request_id)
    if request:
        return request
    raise HTTPException(status_code=404, detail="Request not found")

@router.post("/", response_model=RequestInDB)
async def add_request(request: RequestCreate):
    return await create_request(request)

@router.put("/{request_id}", response_model=RequestInDB)
async def modify_request(request_id: int, request: RequestUpdate):
    updated_request = await update_request(request_id, request)
    if updated_request:
        return updated_request
    raise HTTPException(status_code=404, detail="Request not found")

@router.delete("/{request_id}", response_model=dict)
async def remove_request(request_id: int):
    result = await delete_request(request_id)
    if result:
        return {"message": "Request successfully deleted"}
    raise HTTPException(status_code=404, detail="Request not found")
