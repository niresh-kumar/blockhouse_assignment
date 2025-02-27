from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import database
import models
from database import get_db

#comment 1
app = FastAPI(
    title="Trading API",
    description="A simple trading API with order management and real-time updates.",
    version="1.0.0"
)

class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

    class Config:
        schema_extra = {
            "example": {
                "symbol": "AAPL",
                "price": 150.5,
                "quantity": 10,
                "order_type": "buy"
            }
        }

# Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

# Store WebSocket connections for real-time updates
websocket_clients = []


@app.post("/orders", response_model=OrderCreate, summary="Create a new order")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        symbol=order.symbol,
        price=order.price,
        quantity=order.quantity,
        order_type=order.order_type
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Notify WebSocket clients
    order_data = {
        "id": db_order.id,
        "symbol": db_order.symbol,
        "price": db_order.price,
        "quantity": db_order.quantity,
        "order_type": db_order.order_type
    }
    for client in websocket_clients:
        await client.send_json({"event": "new_order", "data": order_data})

    return order


@app.get("/orders", response_model=List[OrderCreate], summary="Get all orders")
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return [{"symbol": o.symbol, "price": o.price, "quantity": o.quantity, "order_type": o.order_type} for o in orders]

# WebSocket endpoint for real-time updates
@app.websocket("/ws/orders")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            # Keep connection alive; client can disconnect anytime
            await websocket.receive_text()
    except Exception:
        websocket_clients.remove(websocket)
        await websocket.close()



# Run with: uvicorn main:app --reload