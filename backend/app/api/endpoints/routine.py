from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
import uuid
from typing import List

from app.db.session import get_db
from app.models.routine import RoutineAnalysis
from app.core.auth import verify_firebase_token
from app.services.ai_gateway.gateway import gateway

router = APIRouter()

class RoutineRequest(BaseModel):
    text: str

class RoutineResponse(BaseModel):
    id: str
    original_text: str
    estimated_carbon_kg: float
    transport_impact: float
    electricity_impact: float
    food_impact: float
    other_impact: float
    eco_score: float
    recommendations: list

    class Config:
        orm_mode = True

@router.post("/", response_model=RoutineResponse)
async def analyze_routine(
    req: RoutineRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Call Gemini to analyze routine
    try:
        analysis = await gateway.analyze_routine(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    import json
    entry = RoutineAnalysis(
        id=str(uuid.uuid4()),
        user_id=uid,
        original_text=req.text,
        estimated_carbon_kg=analysis.get("estimatedCarbonKg", 0.0),
        transport_impact=analysis.get("transportImpact", 0.0),
        electricity_impact=analysis.get("electricityImpact", 0.0),
        food_impact=analysis.get("foodImpact", 0.0),
        other_impact=analysis.get("otherImpact", 0.0),
        eco_score=analysis.get("ecoScore", 0.0),
        recommendations=json.dumps(analysis.get("recommendations", []))
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return {
        "id": entry.id,
        "original_text": entry.original_text,
        "estimated_carbon_kg": entry.estimated_carbon_kg,
        "transport_impact": entry.transport_impact,
        "electricity_impact": entry.electricity_impact,
        "food_impact": entry.food_impact,
        "other_impact": entry.other_impact,
        "eco_score": entry.eco_score,
        "recommendations": analysis.get("recommendations", [])
    }

@router.get("/", response_model=List[RoutineResponse])
async def get_routine_history(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    result = await db.execute(select(RoutineAnalysis).where(RoutineAnalysis.user_id == uid).order_by(desc(RoutineAnalysis.created_at)))
    entries = result.scalars().all()
    
    import json
    return [
        {
            "id": e.id,
            "original_text": e.original_text,
            "estimated_carbon_kg": e.estimated_carbon_kg,
            "transport_impact": e.transport_impact,
            "electricity_impact": e.electricity_impact,
            "food_impact": e.food_impact,
            "other_impact": e.other_impact,
            "eco_score": e.eco_score,
            "recommendations": json.loads(e.recommendations) if e.recommendations else []
        } for e in entries
    ]
