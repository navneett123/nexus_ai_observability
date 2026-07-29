import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


model = load("services/model-service/app/main.py", "model_app")
metrics = load("services/metrics-service/app/main.py", "metrics_app")
dashboard = load("services/dashboard/app/main.py", "dashboard_app")


def test_models():
    response = TestClient(model.app).get("/models")
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_metrics():
    response = TestClient(metrics.app).get("/metrics/supportpilot")
    assert response.status_code == 200
    assert "gpu_utilization" in response.json()["summary"]


def test_missing_model():
    assert TestClient(model.app).get("/models/missing").status_code == 404



def test_model_health_version():
    response = TestClient(model.app).get("/health")
    assert response.status_code == 200
    assert response.json()["version"] == model.APP_VERSION


def test_metrics_health_version():
    response = TestClient(metrics.app).get("/health")
    assert response.status_code == 200
    assert response.json()["version"] == metrics.APP_VERSION

def test_dashboard_health():
    response = TestClient(dashboard.app).get("/health")
    assert response.status_code == 200
    assert response.json()["version"] == dashboard.APP_VERSION


def test_dashboard_page_uses_platform_health_section():
    response = TestClient(dashboard.app).get("/")
    assert response.status_code == 200
    assert "Platform service health" in response.text
    assert "/static/dashboard.js" in response.text


def test_platform_health_operational(monkeypatch):
    async def healthy_service(_client, name, _url):
        return {"name": name, "status": "healthy", "latency_ms": 1.0, "status_code": 200}

    monkeypatch.setattr(dashboard, "check_service", healthy_service)
    response = TestClient(dashboard.app).get("/api/platform-health")
    payload = response.json()
    assert response.status_code == 200
    assert payload["overall_status"] == "operational"
    assert payload["healthy_services"] == 3