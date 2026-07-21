import os, httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

MODEL_SERVICE_URL=os.getenv("MODEL_SERVICE_URL","http://model-service:8001")
METRICS_SERVICE_URL=os.getenv("METRICS_SERVICE_URL","http://metrics-service:8002")
APP_VERSION=os.getenv("APP_VERSION","local")
ENVIRONMENT_NAME=os.getenv("ENVIRONMENT_NAME","Local")
OCTOPUS_RELEASE=os.getenv("OCTOPUS_RELEASE","local")
KUBERNETES_NAMESPACE=os.getenv("KUBERNETES_NAMESPACE","local")
REFRESH_INTERVAL=int(os.getenv("REFRESH_INTERVAL","8"))
DEFAULT_MODEL=os.getenv("DEFAULT_MODEL","supportpilot")

app=FastAPI(title="Nexus AI Observability",version="2.0.0")
app.mount("/static",StaticFiles(directory="app/static"),name="static")
templates=Jinja2Templates(directory="app/templates")

@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("dashboard.html",{"request":request,"app_version":APP_VERSION,"environment":ENVIRONMENT_NAME,"release":OCTOPUS_RELEASE,"namespace":KUBERNETES_NAMESPACE,"refresh_interval":REFRESH_INTERVAL,"default_model":DEFAULT_MODEL})
@app.get("/health")
async def health(): return {"status":"healthy","service":"dashboard"}
@app.get("/ready")
async def ready():
    try:
        async with httpx.AsyncClient(timeout=4) as client:
            a=await client.get(f"{MODEL_SERVICE_URL}/health");b=await client.get(f"{METRICS_SERVICE_URL}/health")
        if a.status_code!=200 or b.status_code!=200: raise RuntimeError
        return {"status":"ready"}
    except Exception as exc: raise HTTPException(status_code=503,detail="Dependent service unavailable") from exc
@app.get("/api/models")
async def models():
    async with httpx.AsyncClient(timeout=5) as client:r=await client.get(f"{MODEL_SERVICE_URL}/models")
    if r.status_code!=200: raise HTTPException(status_code=502,detail="Model service unavailable")
    return r.json()
@app.get("/api/models/{model_id}/dashboard")
async def dashboard(model_id:str):
    async with httpx.AsyncClient(timeout=5) as client:
        m=await client.get(f"{MODEL_SERVICE_URL}/models/{model_id}");x=await client.get(f"{METRICS_SERVICE_URL}/metrics/{model_id}")
    if m.status_code==404 or x.status_code==404: raise HTTPException(status_code=404,detail="Model not found")
    if m.status_code!=200 or x.status_code!=200: raise HTTPException(status_code=502,detail="Backend unavailable")
    model=m.json();data=x.json();data["model"]=model
    data["summary"]["business_metric"]={"label":model["business_metric"],"value":data["summary"].pop("business_value"),"unit":model["business_unit"]}
    data["deployment"]={"environment":ENVIRONMENT_NAME,"application_version":APP_VERSION,"octopus_release":OCTOPUS_RELEASE,"namespace":KUBERNETES_NAMESPACE}
    return data
