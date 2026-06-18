# purpose: Carbon Router | enforces: Security-first
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.carbon_intelligence.calculator import CarbonCalculator
from app.services.carbon_intelligence.benchmarking import BenchmarkingService

router = APIRouter()

class CarbonEntryRequest(BaseModel):
    activityType: str
    value: float
    unit: str

@router.post("/calculate")
async def calculate_carbon(entry: CarbonEntryRequest):
    co2e = CarbonCalculator.calculate(entry.activityType, entry.value)
    return {"co2e_kg": co2e}

@router.get("/benchmarks")
async def get_benchmark(co2e_kg: float):
    percentile = BenchmarkingService.get_percentile(co2e_kg)
    return {"percentile": percentile}
