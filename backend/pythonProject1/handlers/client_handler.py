from fastapi import APIRouter, HTTPException
from typing import List
from models import Client
from db import clients_collection

router = APIRouter()

@router.get("/clients", response_model=List[Client])
async def get_clients():
    clients = list(clients_collection.find())
    return clients

@router.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: int):
    client = clients_collection.find_one({"_id": client_id})
    if client:
        return client
    raise HTTPException(status_code=404, detail="Client not found")

@router.post("/clients/", response_model=Client)
async def create_client(client: Client):
    clients_collection.insert_one(client.dict())
    return client

@router.put("/clients/{client_id}", response_model=Client)
async def update_client(client_id: int, client: Client):
    existing_client = clients_collection.find_one({"_id": client_id})
    if existing_client:
        updated_client = {**existing_client, **client.dict()}
        clients_collection.update_one({"_id": client_id}, {"$set": updated_client})
        return updated_client
    raise HTTPException(status_code=404, detail="Client not found")

@router.delete("/clients/{client_id}", response_model=dict)
async def delete_client(client_id: int):
    result = clients_collection.delete_one({"_id": client_id})
    if result.deleted_count == 1:
        return {"message": "Client deleted successfully"}
    raise HTTPException(status_code=404, detail="Client not found")
