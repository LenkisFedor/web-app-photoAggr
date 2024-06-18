from fastapi import APIRouter, HTTPException
from typing import List
from schemas.order import OrderCreate, OrderUpdate, OrderInDB
from crud.order import get_orders, get_order, create_order, update_order, delete_order

router = APIRouter()

@router.get("/", response_model=List[OrderInDB])
async def read_orders():
    return await get_orders()

@router.get("/{order_id}", response_model=OrderInDB)
async def read_order(order_id: int):
    order = await get_order(order_id)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")

@router.post("/", response_model=OrderInDB)
async def add_order(order: OrderCreate):
    return await create_order(order)

@router.put("/{order_id}", response_model=OrderInDB)
async def modify_order(order_id: int, order: OrderUpdate):
    updated_order = await update_order(order_id, order)
    if updated_order:
        return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/{order_id}", response_model=dict)
async def remove_order(order_id: int):
    result = await delete_order(order_id)
    if result:
        return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")
