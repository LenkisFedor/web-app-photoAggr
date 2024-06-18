from fastapi import HTTPException
from db import orders_collection
from models.order import Order
from schemas.order import OrderInDB, OrderCreate, OrderUpdate
from utils.sequences import get_next_sequence_value
from typing import List




async def get_orders() -> List[OrderInDB]:
    orders = orders_collection.find()
    return [OrderInDB(**order) for order in orders]


async def get_order(order_id: int) -> OrderInDB:
    order = orders_collection.find_one({"_id": order_id})
    if order:
        return OrderInDB(**order)
    raise HTTPException(status_code=404, detail="Order not found")


async def create_order(order_data: OrderCreate) -> OrderInDB:
    order_id = get_next_sequence_value("orders")
    order_dict = order_data.dict()
    order_dict["_id"] = order_id
    orders_collection.insert_one(order_dict)
    return OrderInDB(**order_dict)


async def update_order(order_id: int, order_data: OrderUpdate) -> OrderInDB:
    existing_order = orders_collection.find_one({"_id": order_id})
    if existing_order:
        updated_order_data = order_data.dict(exclude_unset=True)
        updated_order = {**existing_order, **updated_order_data}
        orders_collection.update_one({"_id": order_id}, {"$set": updated_order})
        return OrderInDB(**updated_order)
    raise HTTPException(status_code=404, detail="Order not found")


async def delete_order(order_id: str):
    result = orders_collection.delete_one({"_id": order_id})
    if result.deleted_count == 1:
        return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")
