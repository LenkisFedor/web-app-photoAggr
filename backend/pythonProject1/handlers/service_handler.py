from fastapi import APIRouter, HTTPException
from bson import ObjectId
from db import services_collection
from models import Service

router = APIRouter()

@router.get("/services", response_model=list[Service])
def get_services():
    services = list(services_collection.find())
    for serv in services:
        serv['_id'] = str(serv['_id'])
    return services

@router.get("/services/{service_id}", response_model=Service)
def get_service(service_id: str):
    service = services_collection.find_one({"_id": ObjectId(service_id)})
    if service:
        service['_id'] = str(service['_id'])
        return service
    else:
        raise HTTPException(status_code=404, detail="Service not found")

@router.post("/services/", response_model=dict)
def create_service(service: Service):
    service_data = service.dict()
    service_id = services_collection.insert_one(service_data).inserted_id
    return {"message": "Service created successfully", "service_id": str(service_id)}

@router.put("/services/{service_id}", response_model=dict)
def update_service(service_id: str, service: Service):
    service_data = service.dict()
    result = services_collection.update_one({"_id": ObjectId(service_id)}, {"$set": service_data})
    if result.modified_count == 1:
        return {"message": "Service updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Service not found")

@router.delete("/services/{service_id}", response_model=dict)
def delete_service(service_id: str):
    result = services_collection.delete_one({"_id": ObjectId(service_id)})
    if result.deleted_count == 1:
        return {"message": "Service deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Service not found")
