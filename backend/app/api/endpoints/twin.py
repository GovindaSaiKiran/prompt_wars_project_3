from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Dict

from app.db.session import get_db
from app.models.carbon import CarbonEntry
from app.core.auth import verify_firebase_token

router = APIRouter()

class TwinScenario(BaseModel):
    variables: Dict[str, float] # e.g. {"transport": 0.5} means 50% reduction in transport

@router.post("/simulate")
async def simulate_twin(
    scenario: TwinScenario,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    
    # Calculate baseline
    result = await db.execute(select(CarbonEntry).where(CarbonEntry.user_id == uid))
    entries = result.scalars().all()
    
    breakdown = {}
    total_baseline = 0.0
    for e in entries:
        cat = e.category
        val = e.co2e_kg
        breakdown[cat] = breakdown.get(cat, 0.0) + val
        total_baseline += val
        
    simulated_total = total_baseline
    
    for category, reduction_pct in scenario.variables.items():
        if category in breakdown:
            saved = breakdown[category] * reduction_pct
            simulated_total -= saved
            
    return {
        "baseline_co2e": total_baseline,
        "simulated_co2e": simulated_total,
        "difference": simulated_total - total_baseline
    }
