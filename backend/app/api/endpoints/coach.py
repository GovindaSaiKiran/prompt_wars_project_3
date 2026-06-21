# purpose: AI Coach Router | enforces: Security-first
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import uuid

from app.db.session import get_db
from app.core.auth import verify_firebase_token
from app.services.ai_gateway.gateway import gateway
from pydantic import BaseModel

from app.models.coach import ConversationMessage
from app.models.carbon import CarbonEntry
from app.models.goal import Goal

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

async def get_coach_context(uid: str, db: AsyncSession):
    # Fetch recent carbon history
    carbon_res = await db.execute(select(CarbonEntry).where(CarbonEntry.user_id == uid).order_by(desc(CarbonEntry.created_at)).limit(10))
    carbons = carbon_res.scalars().all()
    
    # Fetch goals
    goal_res = await db.execute(select(Goal).where(Goal.user_id == uid).limit(10))
    goals = goal_res.scalars().all()

    # We could also fetch analytics, but for now we summarize the basic data.
    return {
        "recent_emissions": [{"category": c.category, "amount": c.amount, "carbon": c.carbon_calculated} for c in carbons],
        "goals": [{"title": g.title, "target": g.target_reduction, "progress": g.current_progress} for g in goals]
    }

async def get_chat_history(uid: str, db: AsyncSession):
    msg_res = await db.execute(select(ConversationMessage).where(ConversationMessage.user_id == uid).order_by(desc(ConversationMessage.created_at)).limit(5))
    msgs = msg_res.scalars().all()
    msgs.reverse() # chronological order
    return [{"role": m.role, "content": m.content} for m in msgs]

@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Save user message
    user_msg = ConversationMessage(id=str(uuid.uuid4()), user_id=uid, role="user", content=request.message)
    db.add(user_msg)
    await db.commit()

    context = await get_coach_context(uid, db)
    history = await get_chat_history(uid, db)

    async def stream_and_save():
        full_response = ""
        async for chunk in gateway.stream_coach_response(request.message, context, history):
            full_response += chunk
            yield chunk
            
        # Save AI response
        ai_msg = ConversationMessage(id=str(uuid.uuid4()), user_id=uid, role="assistant", content=full_response)
        db.add(ai_msg)
        await db.commit()

    return StreamingResponse(stream_and_save(), media_type="text/event-stream")

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")
        
    user_msg = ConversationMessage(id=str(uuid.uuid4()), user_id=uid, role="user", content=request.message)
    db.add(user_msg)
    await db.commit()

    context = await get_coach_context(uid, db)
    history = await get_chat_history(uid, db)
    
    response = await gateway.generate_coach_response(request.message, context, history)
    
    ai_msg = ConversationMessage(id=str(uuid.uuid4()), user_id=uid, role="assistant", content=response.get("recommendation", "Error"))
    db.add(ai_msg)
    await db.commit()
    
    return response

@router.get("/history")
async def get_history(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    history = await get_chat_history(uid, db)
    return history
