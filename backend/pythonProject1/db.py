import os
import psycopg2
from pymongo import MongoClient

# Подключение к MongoDB
mongo_host = os.getenv("MONGO_HOST", "mongodb")
mongo_port = int(os.getenv("MONGO_PORT", 27017))
mongo_db = os.getenv("MONGO_INITDB_DATABASE", "photo_aggr")
client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
db = client[mongo_db]

photographers_collection = db["photographers"]
clients_collection = db["clients"]
orders_collection = db["orders"]
services_collection = db["services"]
requests_collection = db["requests"]

# Подключение к PostgreSQL
postgres_host = os.getenv("POSTGRES_HOST", "postgres")
postgres_user = os.getenv("POSTGRES_USER", "postgres")
postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
postgres_db = os.getenv("POSTGRES_DB", "employees")

def get_postgres_connection():
    return psycopg2.connect(
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
        host=postgres_host
    )

# Коллекция employees из PostgreSQL
def get_employees_collection():
    conn = get_postgres_connection()
    cur = conn.cursor()
    return conn, cur
