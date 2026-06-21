import hmac
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from pydantic import BaseModel

from app.db.session import get_db
from app.models.leaderboard import LeaderboardEntry
from app.core.auth import verify_firebase_token
from app.core.config import settings

router = APIRouter()

class LeaderboardResponse(BaseModel):
    id: str
    user_id: str
    username: str
    score: float
    reduction_pct: float
    streak: int
    region: str
    emoji: str
    rank: int

class LeaderboardUpdateRequest(BaseModel):
    username: str
    score: float
    reduction_pct: float
    streak: int
    region: str
    emoji: str
    signature: str

def verify_signature(data: str, signature: str) -> bool:
    expected_hmac = hmac.new(
        settings.gemini_api_key.encode(), # using an existing secret for HMAC
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_hmac, signature)

@router.get("/", response_model=List[LeaderboardResponse])
async def get_leaderboard(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LeaderboardEntry).order_by(desc(LeaderboardEntry.score)).limit(100)
    )
    entries = result.scalars().all()
    
    response = []
    for i, entry in enumerate(entries):
        response.append(LeaderboardResponse(
            id=entry.id,
            user_id=entry.user_id,
            username=entry.username,
            score=entry.score,
            reduction_pct=entry.reduction_pct,
            streak=entry.streak,
            region=entry.region,
            emoji=entry.emoji,
            rank=i + 1
        ))
    return response

@router.post("/", response_model=LeaderboardResponse)
async def update_leaderboard(
    req: LeaderboardUpdateRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    
    # Payload for signature verification
    payload = f"{uid}:{int(req.score)}:{req.streak}"
    print(f"DEBUG: payload={payload}, req.sig={req.signature}")
    if not verify_signature(payload, req.signature):
        raise HTTPException(status_code=403, detail="Invalid HMAC signature. Data tampered.")
        
    result = await db.execute(select(LeaderboardEntry).where(LeaderboardEntry.user_id == uid))
    entry = result.scalars().first()
    
    if entry:
        entry.score = req.score
        entry.reduction_pct = req.reduction_pct
        entry.streak = req.streak
        entry.signature = req.signature
    else:
        entry = LeaderboardEntry(
            id=uid,
            user_id=uid,
            username=req.username,
            score=req.score,
            reduction_pct=req.reduction_pct,
            streak=req.streak,
            region=req.region,
            emoji=req.emoji,
            signature=req.signature
        )
        db.add(entry)
        
    await db.commit()
    
    # We return an estimated rank of 0 because calculating precise rank on update requires full scan
    # It will be accurate on GET /leaderboard
    return LeaderboardResponse(
        id=entry.id,
        user_id=entry.user_id,
        username=entry.username,
        score=entry.score,
        reduction_pct=entry.reduction_pct,
        streak=entry.streak,
        region=entry.region,
        emoji=entry.emoji,
        rank=0
    )
