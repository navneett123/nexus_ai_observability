import asyncio
import os
import time
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://model-service:8001")
METRICS_SERVICE_URL = os.getenv("METRICS_SERVICE_URL", "http://metrics-service:8002")
APP_VERSION = os.getenv("APP_VERSION", "local")
ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "Local")
OCTOPUS_RELEASE = os.getenv("OCTOPUS_RELEASE", "local")
KUBERNETES_NAMESPACE = os.getenv("KUBERNETES_NAMESPACE", "local")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "8"))
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "supportpilot")

app = FastAPI(title="Nexus AI Observability", version="2.1.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "app_version": APP_VERSION,
            "environment": ENVIRONMENT_NAME,
            "release": OCTOPUS_RELEASE,
            "namespace": KUBERNETES_NAMESPACE,
            "refresh_interval": REFRESH_INTERVAL,
            "default_model": DEFAULT_MODEL,
        },
    )


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "dashboard", "version": app.version}


async def check_service(client: httpx.AsyncClient, name: str, url: str) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        response = await client.get(f"{url}/health")
        latency_ms = round((time.perf_counter() - started) * 1000, 1)
        healthy = response.status_code == 200
        return {
            "name": name,
            "status": "healthy" if healthy else "unhealthy",
            "latency_ms": latency_ms,
            "status_code": response.status_code,
        }
    except httpx.HTTPError:
        latency_ms = round((time.perf_counter() - started) * 1000, 1)
        return {
            "name": name,
            "status": "unreachable",
            "latency_ms": latency_ms,
            "status_code": None,
        }


@app.get("/api/platform-health")
async def platform_health():
    dashboard_status = {
        "name": "Dashboard service",
        "status": "healthy",
        "latency_ms": 0.0,
        "status_code": 200,
    }

    async with httpx.AsyncClient(timeout=4) as client:
        model_status, metrics_status = await asyncio.gather(
            check_service(client, "Model service", MODEL_SERVICE_URL),
            check_service(client, "Metrics service", METRICS_SERVICE_URL),
        )

    services = [dashboard_status, model_status, metrics_status]
    healthy_count = sum(service["status"] == "healthy" for service in services)

    if healthy_count == len(services):
        overall = "operational"
    elif healthy_count == 0:
        overall = "outage"
    else:
        overall = "degraded"

    return {
        "overall_status": overall,
        "healthy_services": healthy_count,
        "total_services": len(services),
        "services": services,
        "environment": ENVIRONMENT_NAME,
        "namespace": KUBERNETES_NAMESPACE,
    }


@app.get("/ready")
async def ready():
    health_data = await platform_health()
    if health_data["overall_status"] != "operational":
        raise HTTPException(status_code=503, detail="Dependent service unavailable")
    return {"status": "ready"}


@app.get("/api/models")
async def models():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{MODEL_SERVICE_URL}/models")
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Model service unavailable") from exc

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Model service unavailable")
    return response.json()


@app.get("/api/models/{model_id}/dashboard")
async def dashboard(model_id: str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            model_response, metrics_response = await asyncio.gather(
                client.get(f"{MODEL_SERVICE_URL}/models/{model_id}"),
                client.get(f"{METRICS_SERVICE_URL}/metrics/{model_id}"),
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Backend unavailable") from exc

    if model_response.status_code == 404 or metrics_response.status_code == 404:
        raise HTTPException(status_code=404, detail="Model not found")
    if model_response.status_code != 200 or metrics_response.status_code != 200:
        raise HTTPException(status_code=502, detail="Backend unavailable")

    model = model_response.json()
    data = metrics_response.json()
    data["model"] = model
    data["summary"]["business_metric"] = {
        "label": model["business_metric"],
        "value": data["summary"].pop("business_value"),
        "unit": model["business_unit"],
    }
    data["deployment"] = {
        "environment": ENVIRONMENT_NAME,
        "application_version": APP_VERSION,
        "octopus_release": OCTOPUS_RELEASE,
        "namespace": KUBERNETES_NAMESPACE,
    }
    return data