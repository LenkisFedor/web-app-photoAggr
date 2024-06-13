import os

from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import psycopg2

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Здесь можно указать список разрешенных доменов
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Подключение к MongoDB

mongo_host = os.getenv("MONGO_HOST", "mongodb")
mongo_port = int(os.getenv("MONGO_PORT", 27017))
mongo_db = os.getenv("MONGO_INITDB_DATABASE", "photo_aggr")
client = MongoClient(f"mongodb://mongodb-1:{mongo_port}/")
db = client['photo_aggr']
services_collection = db["services"]
orders_collection = db['orders']
clients_collection = db['clients']
requests_collection = db['requests']
photographers_collection = db['photographers']


postgres_host = os.getenv("POSTGRES_HOST", "postgres")
postgres_user = os.getenv("POSTGRES_USER", "postgres")
postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
postgres_db = os.getenv("POSTGRES_DB", "employees")

conn = psycopg2.connect(
    dbname=postgres_db,
    user=postgres_user,
    password=postgres_password,
    host=postgres_host
)
cur = conn.cursor()

class Request(BaseModel):
    client_id: int
    date_requested: str
    type: str
    location: str


class Employee(BaseModel):
    name: str
    role: str
    email: str
    phone: str
    department: str

def get_next_sequence_value(collection_name):
    max_id = db[collection_name].find_one({}, sort=[('_id', -1)])['_id']
    return max_id + 1 if max_id is not None else 1

@app.get("/services")
def get_services():
    services = list(services_collection.find())
    for serv in services:
        serv['_id'] = str(serv['_id'])
    return services

@app.get("/clients")
def get_clients():
    clients = list(clients_collection.find())
    for client in clients:
        client['_id'] = str(client['_id'])
    return clients

@app.get("/clients/{client_id}")
def get_client(client_id: str):
    client = clients_collection.find_one({"_id": ObjectId(client_id)})
    if client:
        client['_id'] = str(client['_id'])
        return client
    else:
        raise HTTPException(status_code=404, detail="Client not found")
    
@app.get("/orders")
def get_orders():
    orders = list(orders_collection.find())
    for order in orders:
        order['_id'] = str(order['_id'])
    return orders

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    if order:
        order['_id'] = str(order['_id'])
        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")


@app.get("/requests")
def get_requests():
    requests = list(requests_collection.find())
    return requests

# Эндпоинт для добавления запроса в базу данных MongoDB
@app.post("/requests/")
def create_request(request: Request):
    request_id = get_next_sequence_value('requests')
    request_data = request.dict()
    request_data['_id'] = request_id
    requests_collection.insert_one(request_data)
    return {"message": "Request created successfully", "request_id": str(request_id)}


# Эндпоинт для удаления запроса из базы данных MongoDB
@app.delete("/requests/{request_id}")
def delete_request(request_id: str):
    result = requests_collection.delete_one({"_id": int(request_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": "Request deleted successfully"}

@app.get("/photographers")
def get_photographers():
    photographers = list(photographers_collection.find())
    for photographer in photographers:
        photographer['_id'] = str(photographer['_id'])
    return photographers

@app.get("/photographers/{photographer_id}")
def get_photographer(photographer_id: str):
    photographer = photographers_collection.find_one({"_id": ObjectId(photographer_id)})
    if photographer:
        photographer['_id'] = str(photographer['_id'])
        return photographer
    else:
        raise HTTPException(status_code=404, detail="Photographer not found")

# POST /photographers/
@app.post("/photographers/")
def create_photographer(photographer: dict):
    photographer_id = photographers_collection.insert_one(photographer).inserted_id
    return {"message": "Photographer created successfully", "photographer_id": str(photographer_id)}

# PUT /photographers/{photographer_id}
@app.put("/photographers/{photographer_id}")
def update_photographer(photographer_id: str, updated_photographer: dict):
    result = photographers_collection.update_one(
        {"_id": ObjectId(photographer_id)},
        {"$set": updated_photographer}
    )
    if result.modified_count == 1:
        return {"message": "Photographer updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Photographer not found")

# DELETE /photographers/{photographer_id}
@app.delete("/photographers/{photographer_id}")
def delete_photographer(photographer_id: str):
    result = photographers_collection.delete_one({"_id": ObjectId(photographer_id)})
    if result.deleted_count == 1:
        return {"message": "Photographer deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Photographer not found")


# Эндпоинт для удаления сотрудника из базы данных PostgreSQL
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
    conn.commit()
    return {"message": "Employee deleted successfully"}

# Эндпоинт для получения списка сотрудников из PostgreSQL
@app.get("/employees")
def get_employees():
    cur.execute("SELECT * FROM employees;")
    employees = cur.fetchall()
    return employees


# Эндпоинт для добавления сотрудника в базу данных PostgreSQL
@app.post("/employees/")
def create_employee(employee: Employee):
    cur.execute("INSERT INTO employees (name, role, email, phone, department) VALUES (%s, %s, %s, %s, %s)",
                (employee.name, employee.role, employee.email, employee.phone, employee.department))
    conn.commit()
    return {"message": "Employee created successfully"}
