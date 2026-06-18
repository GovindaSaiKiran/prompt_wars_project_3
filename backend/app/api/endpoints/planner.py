# purpose: Sustainability Planner Router | enforces: Quality-first
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Goal(BaseModel):
    title: str
    target_reduction: float

@router.post("/")
async def create_goal(goal: Goal):
    return {"id": "123", "status": "active"}
