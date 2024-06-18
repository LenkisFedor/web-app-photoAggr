from fastapi import APIRouter, HTTPException
from typing import List
from db import clients_collection
from models.client import Client
from utils.sequences import get_next_sequence_value
from schemas.client import ClientInDB, ClientCreate, ClientUpdate


async def get_clients() -> List[ClientInDB]:
    clients = clients_collection.find()
    return [ClientInDB(**client) for client in clients]

async def get_client(client_id: int) -> ClientInDB:
    client = clients_collection.find_one({"_id": client_id})
    if client:
        return ClientInDB(**client)
    raise HTTPException(status_code=404, detail="Client not found")


async def create_client(client_data: ClientCreate) -> ClientInDB:
    client_id = get_next_sequence_value("clients")
    client_dict = client_data.dict()
    client_dict["_id"] = client_id
    clients_collection.insert_one(client_dict)
    return ClientInDB(**client_dict)


async def update_client(client_id: int, client_data: ClientUpdate) -> ClientInDB:
    existing_client = clients_collection.find_one({"_id": client_id})
    if existing_client:
        updated_client_data = client_data.dict(exclude_unset=True)
        updated_client = {**existing_client, **updated_client_data}
        clients_collection.update_one({"_id": client_id}, {"$set": updated_client})
        return ClientInDB(**updated_client)
    raise HTTPException(status_code=404, detail="Client not found")


async def delete_client(client_id: int):
    result = clients_collection.delete_one({"_id": client_id})
    if result.deleted_count == 1:
        return {"message": "Client deleted successfully"}
    raise HTTPException(status_code=404, detail="Client not found")
