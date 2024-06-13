from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers import client_handler, photographer_handler, order_handler, request_handler, service_handler, employee_handler

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретные домены
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Подключение обработчиков (handlers)
app.include_router(client_handler.router, prefix="/clients", tags=["clients"])
app.include_router(photographer_handler.router, prefix="/photographers", tags=["photographers"])
app.include_router(order_handler.router, prefix="/orders", tags=["orders"])
app.include_router(request_handler.router, prefix="/requests", tags=["requests"])
app.include_router(service_handler.router, prefix="/services", tags=["services"])
app.include_router(employee_handler.router, prefix="/employees", tags=["employees"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
