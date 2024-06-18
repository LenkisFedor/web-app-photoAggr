from fastapi import APIRouter, HTTPException
from typing import List
from schemas.service import ServiceCreate, ServiceUpdate, ServiceInDB
from crud.service import get_service, get_services, create_service, update_service, delete_service

router = APIRouter()

@router.get("/", response_model=List[ServiceInDB])
async def read_clients():
    return await get_services()

@router.get("/{service_id}", response_model=ServiceInDB)
async def read_service(service_id: int):
    service = await get_service(service_id)
    if service:
        return service
    raise HTTPException(status_code=404, detail="Service not found")

@router.post("/", response_model=ServiceInDB)
async def add_service(service: ServiceCreate):
    return await create_service(service)

@router.put("/{service_id}", response_model=ServiceInDB)
async def modify_service(service_id: int, service: ServiceUpdate):
    updated_service = await update_service(service_id, service)
    if updated_service:
        return updated_service
    raise HTTPException(status_code=404, detail="Service not found")

@router.delete("/{service_id}", response_model=dict)
async def remove_service(service_id: int):
    result = await delete_service(service_id)
    if result:
        return {"message": "Service deleted successfully"}
    raise HTTPException(status_code=404, detail="Service not found")
