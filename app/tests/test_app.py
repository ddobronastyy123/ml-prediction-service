import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app  # noqa: E402


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_predict_no_features():
    client = app.test_client()
    response = client.post("/predict", json={})
    assert response.status_code == 400


def test_predict_wrong_feature_count():
    client = app.test_client()
    response = client.post("/predict", json={"features": [1.0, 2.0, 3.0, 4.0]})
    assert response.status_code == 400
