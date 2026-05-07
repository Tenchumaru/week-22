from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict():
    response = client.post(
        "/v1/predict",
        json={"features": [5.1, 3.5, 1.4, 0.2]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "class_name" in data
