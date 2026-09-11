from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#Test Home API

def test_home():
    response = client.get("/")
    # status code test
    assert response.status_code == 200
    # response data check 
    assert response.json() == {"message":"Hello rahul"}
    # Test ADD API

def test_add():
    response = client.get("/add?a=5&b=4")
        # status code
    assert response.status_code == 200
    assert response.json() == {"result":9}

