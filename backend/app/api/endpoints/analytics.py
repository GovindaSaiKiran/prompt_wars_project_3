from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timedelta
from typing import List

from app.db.session import get_db
from app.core.auth import verify_firebase_token
from app.models.carbon import CarbonEntry
from app.models.calculator import CalculatorEntry
from app.models.goal import Goal

router = APIRouter()

async def get_analytics_for_period(uid: str, db: AsyncSession, days: int, period_name: str):
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Get carbon entries
    c_res = await db.execute(select(CarbonEntry).where(CarbonEntry.user_id == uid, CarbonEntry.created_at >= since_date))
    carbons = c_res.scalars().all()
    
    # Get calculator entries
    calc_res = await db.execute(select(CalculatorEntry).where(CalculatorEntry.user_id == uid, CalculatorEntry.created_at >= since_date))
    calcs = calc_res.scalars().all()
    
    total_produced = sum(c.carbon_calculated for c in carbons) + sum(calc.carbon_produced_kg for calc in calcs)
    total_saved = sum(calc.eco_alternative_savings_kg for calc in calcs)
    
    # Get goals progress
    goal_res = await db.execute(select(Goal).where(Goal.user_id == uid))
    goals = goal_res.scalars().all()
    total_saved += sum(g.current_progress for g in goals)
    
    # Basic category aggregation
    categories = {}
    for c in carbons:
        categories[c.category] = categories.get(c.category, 0) + c.carbon_calculated
    for calc in calcs:
        categories["transportation"] = categories.get("transportation", 0) + calc.carbon_produced_kg
        
    top_source = max(categories, key=categories.get) if categories else "None"
    
    return {
        "period": period_name,
        "totalCarbonProducedKg": total_produced,
        "totalCarbonSavedKg": total_saved,
        "sustainabilityScore": max(0, 1000 - total_produced),
        "topEmissionSource": top_source,
        "topSavingSource": "Transportation" if calcs else "General Goals"
    }

@router.get("/daily")
async def get_daily(db: AsyncSession = Depends(get_db), token: dict = Depends(verify_firebase_token)):
    return await get_analytics_for_period(token.get("uid"), db, 1, "daily")

@router.get("/weekly")
async def get_weekly(db: AsyncSession = Depends(get_db), token: dict = Depends(verify_firebase_token)):
    return await get_analytics_for_period(token.get("uid"), db, 7, "weekly")

@router.get("/monthly")
async def get_monthly(db: AsyncSession = Depends(get_db), token: dict = Depends(verify_firebase_token)):
    return await get_analytics_for_period(token.get("uid"), db, 30, "monthly")

@router.get("/yearly")
async def get_yearly(db: AsyncSession = Depends(get_db), token: dict = Depends(verify_firebase_token)):
    return await get_analytics_for_period(token.get("uid"), db, 365, "yearly")

@router.get("/trends")
async def get_trends(db: AsyncSession = Depends(get_db), token: dict = Depends(verify_firebase_token)):
    current_week = await get_analytics_for_period(token.get("uid"), db, 7, "current_week")
    past_week = await get_analytics_for_period(token.get("uid"), db, 14, "past_week")
    
    # Adjust past week to only be the 7 days prior
    past_week["totalCarbonProducedKg"] = max(0, past_week["totalCarbonProducedKg"] - current_week["totalCarbonProducedKg"])
    
    trend = 0
    if past_week["totalCarbonProducedKg"] > 0:
        trend = ((current_week["totalCarbonProducedKg"] - past_week["totalCarbonProducedKg"]) / past_week["totalCarbonProducedKg"]) * 100
        
    return {
        "current_week": current_week,
        "past_week": past_week,
        "trend_percent": trend,
        "insights": [
            f"You produced {abs(trend):.1f}% {'more' if trend > 0 else 'less'} carbon this week compared to last week.",
            f"Your top emission source is {current_week['topEmissionSource']}.",
            f"You saved {current_week['totalCarbonSavedKg']:.1f} kg CO₂ so far."
        ]
    }
