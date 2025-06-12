from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.templates import validate_liquid_template
from app.dedupe import DeduplicationCache
from app.braze_client import BrazeClient
import asyncio

app = FastAPI()

dedupe_cache = DeduplicationCache(redis_url="redis://localhost")
braze_client = BrazeClient(api_key="your_braze_api_key_here")

class TemplateValidationRequest(BaseModel):
    template: str
    payloads: List[Dict]

class EventRequest(BaseModel):
    event_id: str
    payload: Dict

@app.post("/validate-template/")
async def validate_template(request: TemplateValidationRequest):
    errors = validate_liquid_template(request.template, request.payloads)
    if errors:
        raise HTTPException(status_code=400, detail=errors)
    return {"status": "valid"}

@app.post("/send-event/")
async def send_event(request: EventRequest):
    if await dedupe_cache.is_duplicate(request.event_id):
        return {"status": "duplicate", "event_id": request.event_id}
    success = await braze_client.send_event(request.payload)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send event to Braze")
    return {"status": "sent"}