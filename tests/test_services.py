import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,Path(path));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
model=load("services/model-service/app/main.py","model_app")
metrics=load("services/metrics-service/app/main.py","metrics_app")
def test_models(): 
    r=TestClient(model.app).get("/models"); assert r.status_code==200 and len(r.json())==6
def test_metrics():
    r=TestClient(metrics.app).get("/metrics/supportpilot"); assert r.status_code==200 and "gpu_utilization" in r.json()["summary"]
def test_missing():
    assert TestClient(model.app).get("/models/missing").status_code==404
