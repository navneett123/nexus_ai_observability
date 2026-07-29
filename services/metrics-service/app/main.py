import math, os, random
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
APP_VERSION = os.getenv("APP_VERSION", "local")
app = FastAPI(title="Nexus AI Metrics Service", version=APP_VERSION)
PROFILES={
"supportpilot":{"latency":1820,"gpu":76,"business":91.4,"tokens":38,"errors":["Context length exceeded","Prompt safety validation failed","Knowledge retrieval timeout"]},
"visionforge":{"latency":76,"gpu":88,"business":97.1,"tokens":0,"errors":["Invalid image dimensions","CUDA out of memory","Camera frame timeout"]},
"fraudguard":{"latency":42,"gpu":18,"business":96.4,"tokens":0,"errors":["Feature data unavailable","Risk scoring timeout","Rules engine unavailable"]},
"documind":{"latency":310,"gpu":62,"business":94.7,"tokens":0,"errors":["Unsupported document format","OCR confidence below threshold","Encrypted document"]},
"echoscribe":{"latency":8200,"gpu":71,"business":94.6,"tokens":0,"errors":["Unsupported audio codec","Transcription timeout","No speech detected"]},
"demandpulse":{"latency":128,"gpu":12,"business":92.8,"tokens":0,"errors":["Insufficient history","Stale source data","Forecast generation failure"]}}
def trend(base,points=24,spread=.12):
    return [round(max(0,base+math.sin(i/2.8)*base*spread+random.uniform(-base*spread/2,base*spread/2)),2) for i in range(points)]
@app.get("/health")
def health(): return {"status":"healthy","service":"metrics-service","version":APP_VERSION}
@app.get("/metrics/{model_id}")
def metrics(model_id:str):
    if model_id not in PROFILES: raise HTTPException(status_code=404,detail="Metrics profile not found")
    p=PROFILES[model_id]; latency=max(1,int(p["latency"]*random.uniform(.92,1.08))); gpu=max(0,min(99,p["gpu"]+random.randint(-6,6)))
    error_rate=round(random.uniform(.25,2.6),2); rps=round(random.uniform(8,48),1); cpu=random.randint(25,78); memory=random.randint(38,84); replicas=random.randint(1,3)
    return {"summary":{"total_requests":random.randint(85000,480000),"requests_per_second":rps,"success_rate":round(100-error_rate,2),"average_latency_ms":latency,"error_rate":error_rate,"gpu_utilization":gpu,"active_replicas":replicas,"business_value":round(p["business"]+random.uniform(-.8,.8),1),"tokens_per_second":p["tokens"]+random.randint(-3,4) if p["tokens"] else None},
    "infrastructure":{"cpu_utilization":cpu,"memory_utilization":memory,"gpu_utilization":gpu,"gpu_memory_utilization":max(0,min(99,gpu+random.randint(-8,10))),"gpu_temperature_c":random.randint(54,81),"gpu_power_w":random.randint(115,285),"running_pods":replicas,"ready_nodes":3,"queue_depth":random.randint(0,36)},
    "inference":{"p50_ms":int(latency*.74),"p95_ms":int(latency*1.65),"p99_ms":int(latency*2.25),"timeouts":random.randint(0,10),"throughput":rps},
    "charts":{"requests":trend(rps,spread=.25),"latency":trend(latency,spread=.18),"gpu":trend(gpu,spread=.10),"errors":[random.randint(0,8) for _ in range(24)]},
    "errors":[{"time":datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),"type":m,"severity":["warning","critical","warning"][i],"count":random.randint(1,18)} for i,m in enumerate(p["errors"])],
    "generated_at":datetime.now(timezone.utc).isoformat()}
