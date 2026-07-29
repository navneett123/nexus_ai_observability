import os
from fastapi import FastAPI, HTTPException

APP_VERSION = os.getenv("APP_VERSION", "local")
app = FastAPI(title="Nexus AI Model Catalog", version=APP_VERSION)

MODELS = {
 "supportpilot":{"id":"supportpilot","name":"SupportPilot Assistant","use_case":"Generative AI assistant for customer-support agents","type":"Large Language Model","framework":"Llama","version":"8B-v6","endpoint":"/inference/support","owner":"Customer Experience AI","accent":"#8b5cf6","business_metric":"Positive feedback","business_unit":"%"},
 "visionforge":{"id":"visionforge","name":"VisionForge Inspector","use_case":"Computer-vision defect detection for manufacturing lines","type":"Computer Vision","framework":"YOLO","version":"5.1","endpoint":"/inference/vision","owner":"Factory Intelligence","accent":"#06b6d4","business_metric":"Detection accuracy","business_unit":"%"},
 "fraudguard":{"id":"fraudguard","name":"Sentinel FraudGuard","use_case":"Real-time fraud detection for card and wallet transactions","type":"Classification","framework":"XGBoost","version":"4.2","endpoint":"/inference/fraud","owner":"Risk Platform","accent":"#f59e0b","business_metric":"Detection accuracy","business_unit":"%"},
 "documind":{"id":"documind","name":"DocuMind Extractor","use_case":"OCR and field extraction from invoices, forms and contracts","type":"Document AI","framework":"PyTorch","version":"3.7","endpoint":"/inference/documents","owner":"Document Automation","accent":"#10b981","business_metric":"Extraction accuracy","business_unit":"%"},
 "echoscribe":{"id":"echoscribe","name":"EchoScribe Speech AI","use_case":"Speech-to-text for contact-centre and meeting audio","type":"Speech-to-Text","framework":"Whisper","version":"2.5","endpoint":"/inference/audio","owner":"Voice Platform","accent":"#ec4899","business_metric":"Transcription accuracy","business_unit":"%"},
 "demandpulse":{"id":"demandpulse","name":"DemandPulse Forecaster","use_case":"Product-demand and inventory forecasting","type":"Time Series","framework":"Prophet","version":"3.3","endpoint":"/inference/forecast","owner":"Supply Intelligence","accent":"#3b82f6","business_metric":"Forecast accuracy","business_unit":"%"}
}
@app.get("/health")
def health(): return {"status":"healthy","service":"model-service","version":APP_VERSION}
@app.get("/models")
def list_models(): return list(MODELS.values())
@app.get("/models/{model_id}")
def get_model(model_id:str):
    if model_id not in MODELS: raise HTTPException(status_code=404, detail="Model not found")
    return MODELS[model_id]
