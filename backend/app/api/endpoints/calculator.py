from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
import uuid
from typing import List

from app.db.session import get_db
from app.models.calculator import CalculatorEntry
from app.core.auth import verify_firebase_token

router = APIRouter()

class CalculatorRequest(BaseModel):
    distance: float
    vehicle_type: str

class CalculatorResponse(BaseModel):
    id: str
    distance: float
    vehicle_type: str
    carbon_produced_kg: float
    money_spent: float
    eco_alternative_savings_kg: float
    eco_alternative_savings_money: float

    class Config:
        orm_mode = True

# Mock lookup for vehicle types to carbon factors and costs
VEHICLE_FACTORS = {
    "Petrol Bike": {"carbon_per_km": 0.04, "cost_per_km": 2.0},
    "Petrol Car": {"carbon_per_km": 0.128, "cost_per_km": 8.5},
    "Diesel Car": {"carbon_per_km": 0.14, "cost_per_km": 7.0},
    "Diesel SUV": {"carbon_per_km": 0.18, "cost_per_km": 10.0},
    "Electric Bike": {"carbon_per_km": 0.005, "cost_per_km": 0.2},
    "Electric Car": {"carbon_per_km": 0.04, "cost_per_km": 1.5},
    "Bus": {"carbon_per_km": 0.02, "cost_per_km": 1.0},
    "Train": {"carbon_per_km": 0.015, "cost_per_km": 0.8},
    "Flight": {"carbon_per_km": 0.25, "cost_per_km": 15.0},
}

@router.post("/", response_model=CalculatorResponse)
async def calculate_carbon(
    req: CalculatorRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")

    factors = VEHICLE_FACTORS.get(req.vehicle_type)
    if not factors:
        raise HTTPException(status_code=400, detail="Unsupported vehicle type")

    carbon_produced = req.distance * factors["carbon_per_km"]
    money_spent = req.distance * factors["cost_per_km"]

    # Assume Bus is the default eco-alternative for savings calculation if worse than Bus
    # If the user is already better than bus (e.g. Electric Bike), savings = 0
    bus_carbon = req.distance * VEHICLE_FACTORS["Bus"]["carbon_per_km"]
    bus_cost = req.distance * VEHICLE_FACTORS["Bus"]["cost_per_km"]

    savings_kg = max(0, carbon_produced - bus_carbon)
    savings_money = max(0, money_spent - bus_cost)

    entry = CalculatorEntry(
        id=str(uuid.uuid4()),
        user_id=uid,
        distance=req.distance,
        vehicle_type=req.vehicle_type,
        carbon_produced_kg=carbon_produced,
        money_spent=money_spent,
        eco_alternative_savings_kg=savings_kg,
        eco_alternative_savings_money=savings_money
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return entry

@router.get("/", response_model=List[CalculatorResponse])
async def get_history(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    result = await db.execute(select(CalculatorEntry).where(CalculatorEntry.user_id == uid).order_by(desc(CalculatorEntry.created_at)))
    return result.scalars().all()
