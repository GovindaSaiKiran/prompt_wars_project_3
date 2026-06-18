# purpose: AI Coach Router | enforces: Security-first
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.services.ai_gateway.gateway import gateway
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(gateway.stream_coach_response(request.message), media_type="text/event-stream")

@router.post("/chat")
async def chat(request: ChatRequest):
    return await gateway.generate_coach_response(request.message)
