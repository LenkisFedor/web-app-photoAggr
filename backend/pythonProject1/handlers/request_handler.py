from fastapi import APIRouter, HTTPException
from bson import ObjectId
from db import requests_collection
from models import Request

router = APIRouter()

@router.get("/requests", response_model=list[Request])
def get_requests():
    requests = list(requests_collection.find())
    for req in requests:
        req['_id'] = str(req['_id'])
    return requests

@router.get("/requests/{request_id}", response_model=Request)
def get_request(request_id: str):
    request = requests_collection.find_one({"_id": int(request_id)})
    if request:
        request['_id'] = str(request['_id'])
        return request
    else:
        raise HTTPException(status_code=404, detail="Request not found")

@router.post("/requests/", response_model=dict)
def create_request(request: Request):
    request_data = request.dict()
    request_id = requests_collection.insert_one(request_data).inserted_id
    return {"message": "Request created successfully", "request_id": str(request_id)}

@router.put("/requests/{request_id}", response_model=dict)
def update_request(request_id: str, request: Request):
    request_data = request.dict()
    result = requests_collection.update_one({"_id": int(request_id)}, {"$set": request_data})
    if result.modified_count == 1:
        return {"message": "Request updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Request not found")

@router.delete("/requests/{request_id}", response_model=dict)
def delete_request(request_id: str):
    result = requests_collection.delete_one({"_id": int(request_id)})
    if result.deleted_count == 1:
        return {"message": "Request deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Request not found")
