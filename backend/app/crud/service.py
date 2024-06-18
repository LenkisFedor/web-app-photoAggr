from fastapi import HTTPException
from db import services_collection
from models.service import Service
from schemas.service import ServiceInDB, ServiceCreate, ServiceUpdate
from utils.sequences import get_next_sequence_value
from typing import List

async def get_services() -> List[ServiceInDB]:
    services = services_collection.find()
    return [ServiceInDB(**service) for service in services]

async def get_service(service_id: int) -> ServiceInDB:
    service = services_collection.find_one({"_id": service_id})
    if service:
        return ServiceInDB(**service)
    raise HTTPException(status_code=404, detail="Service not found")

async def create_service(service_data: ServiceCreate) -> ServiceInDB:
    service_id = get_next_sequence_value("services")
    service_dict = service_data.dict()
    service_dict["_id"] = service_id
    services_collection.insert_one(service_dict)
    return ServiceInDB(**service_dict)

async def update_service(service_id: int, service_data: ServiceUpdate) -> ServiceInDB:
    existing_service = services_collection.find_one({"_id": service_id})
    if existing_service:
        updated_service_data = service_data.dict(exclude_unset=True)
        updated_service = {**existing_service, **updated_service_data}
        services_collection.update_one({"_id": service_id}, {"$set": updated_service})
        return ServiceInDB(**updated_service)
    raise HTTPException(status_code=404, detail="Service not found")

async def delete_service(service_id: int):
    result = services_collection.delete_one({"_id": service_id})
    if result.deleted_count == 1:
        return {"message": "Service deleted successfully"}
    raise HTTPException(status_code=404, detail="Service not found")
