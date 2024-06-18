from fastapi import APIRouter, HTTPException
from typing import List
from schemas.client import ClientCreate, ClientUpdate, ClientInDB
from crud.client import get_clients, get_client, create_client, update_client, delete_client

router = APIRouter()

@router.get("/", response_model=List[ClientInDB])
async def read_clients():
    return await get_clients()

@router.get("/{client_id}", response_model=ClientInDB)
async def read_client(client_id: int):
    client = await get_client(client_id)
    if client:
        return client
    raise HTTPException(status_code=404, detail="Client not found")

@router.post("/", response_model=ClientInDB)
async def add_client(client: ClientCreate):
    return await create_client(client)

@router.put("/{client_id}", response_model=ClientInDB)
async def modify_client(client_id: int, client: ClientUpdate):
    updated_client = await update_client(client_id, client)
    if updated_client:
        return updated_client
    raise HTTPException(status_code=404, detail="Client not found")

@router.delete("/{client_id}", response_model=dict)
async def remove_client(client_id: int):
    result = await delete_client(client_id)
    if result:
        return {"message": "Client deleted successfully"}
    raise HTTPException(status_code=404, detail="Client not found")
