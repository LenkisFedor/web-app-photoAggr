from fastapi import APIRouter, HTTPException
from bson import ObjectId
from db import orders_collection
from models import Order

router = APIRouter()

@router.get("/orders", response_model=list[Order])
def get_orders():
    orders = list(orders_collection.find())
    for order in orders:
        order['_id'] = str(order['_id'])
    return orders

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    if order:
        order['_id'] = str(order['_id'])
        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@router.post("/orders/", response_model=dict)
def create_order(order: Order):
    order_data = order.dict()
    order_id = orders_collection.insert_one(order_data).inserted_id
    return {"message": "Order created successfully", "order_id": str(order_id)}

@router.put("/orders/{order_id}", response_model=dict)
def update_order(order_id: str, order: Order):
    order_data = order.dict()
    result = orders_collection.update_one({"_id": ObjectId(order_id)}, {"$set": order_data})
    if result.modified_count == 1:
        return {"message": "Order updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{order_id}", response_model=dict)
def delete_order(order_id: str):
    result = orders_collection.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count == 1:
        return {"message": "Order deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Order not found")
