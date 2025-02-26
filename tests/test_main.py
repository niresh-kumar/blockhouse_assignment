from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_order():
    order_data = {"symbol": "AAPL", "price": 150.5, "quantity": 10, "order_type": "buy"}
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    assert response.json() == order_data
