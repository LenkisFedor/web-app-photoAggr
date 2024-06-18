from routers import client_router, service_router, order_router, request_router, phototgrapher_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(client_router.router, prefix="/clients", tags=["clients"])
app.include_router(phototgrapher_router.router, prefix="/photographers", tags=["photographers"])
app.include_router(order_router.router, prefix="/orders", tags=["orders"])
app.include_router(request_router.router, prefix="/requests", tags=["requests"])
app.include_router(service_router.router, prefix="/services", tags=["services"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
