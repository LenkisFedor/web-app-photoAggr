from fastapi import HTTPException
from db import requests_collection
from models.request import Request
from schemas.request import RequestInDB, RequestCreate, RequestUpdate
from utils.sequences import get_next_sequence_value
from typing import List

async def get_requests() -> List[RequestInDB]:
    requests = requests_collection.find()
    return [RequestInDB(**request) for request in requests]

async def get_request(request_id: int) -> RequestInDB:
    request = requests_collection.find_one({"_id": request_id})
    if request:
        return RequestInDB(**request)
    raise HTTPException(status_code=404, detail="Request not found")

async def create_request(request_data: RequestCreate) -> RequestInDB:
    request_id = get_next_sequence_value("requests")
    request_dict = request_data.dict()
    request_dict["_id"] = request_id
    requests_collection.insert_one(request_dict)
    return RequestInDB(**request_dict)

async def update_request(request_id: int, request_data: RequestUpdate) -> RequestInDB:
    existing_request = requests_collection.find_one({"_id": request_id})
    if existing_request:
        updated_request_data = request_data.dict(exclude_unset=True)
        updated_request = {**existing_request, **updated_request_data}
        requests_collection.update_one({"_id": request_id}, {"$set": updated_request})
        return RequestInDB(**updated_request)
    raise HTTPException(status_code=404, detail="Request not found")

async def delete_request(request_id: int):
    result = requests_collection.delete_one({"_id": request_id})
    if result.deleted_count == 1:
        return {"message": "Request deleted successfully"}
    raise HTTPException(status_code=404, detail="Request not found")
