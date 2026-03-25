from fastapi.testclient import TestClient
from src.predict import app

client=TestClient(app)

def test_home_route():
    response=client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_predict_route_valid_input():
    payload={
        'machine_age_days': 200,
        'temperature': 50.3,
        'vibration': 20.2,
        'pressure': 20.1,
        'section': "Cement Mill",
        'component': "Ball Mill",
        'subcomponent': "Gearbox",
    }

    response=client.post("/predict",json=payload)
    assert response.status_code == 200
    data=response.json


def test_predict_route_invalid_input(): 
    payload={
        'machine_age_days': 200,
        'temperature': 50.3,
        'vibration': 20.2,
    }

    response=client.post("/predict",json=payload)
    assert response.status_code == 422


