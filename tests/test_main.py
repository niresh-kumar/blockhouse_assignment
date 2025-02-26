import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)

def mock_get_db():
    class MockSession:
        def query(self, *args):
            return self
        def all(self):
            return []
        def add(self, *args):
            pass
        def commit(self):
            pass
        def refresh(self, *args):
            pass
    yield MockSession()

def test_get_orders():
    with patch('main.get_db', mock_get_db):
        response = client.get("/orders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_create_order():
    with patch('main.get_db', mock_get_db):
        order_data = {"symbol": "AAPL", "price": 150.5, "quantity": 10, "order_type": "buy"}
        response = client.post("/orders", json=order_data)
        assert response.status_code == 200
        assert response.json() == order_data