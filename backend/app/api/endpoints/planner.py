from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.db.session import get_db
from app.models.goal import Goal
from app.core.auth import verify_firebase_token

router = APIRouter()

class GoalCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    goal_type: str = "daily"
    target_reduction: float
    deadline: Optional[datetime] = None

class GoalResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    goal_type: str
    target_reduction: float
    current_progress: float
    status: str
    deadline: Optional[datetime]

    class Config:
        orm_mode = True

@router.post("/", response_model=GoalResponse)
async def create_goal(
    goal_req: GoalCreateRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")

    new_goal = Goal(
        id=str(uuid.uuid4()),
        user_id=uid,
        title=goal_req.title,
        description=goal_req.description,
        goal_type=goal_req.goal_type,
        target_reduction=goal_req.target_reduction,
        deadline=goal_req.deadline
    )
    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)
    
    return new_goal

@router.get("/", response_model=List[GoalResponse])
async def list_goals(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    result = await db.execute(select(Goal).where(Goal.user_id == uid))
    goals = result.scalars().all()
    return goals

class GoalProgressRequest(BaseModel):
    progress_increment: float

@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal_progress(
    goal_id: str,
    req: GoalProgressRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    result = await db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == uid))
    goal = result.scalars().first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
        
    goal.current_progress += req.progress_increment
    if goal.current_progress >= goal.target_reduction:
        goal.status = "completed"
        
    await db.commit()
    await db.refresh(goal)
    return goal

@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    result = await db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == uid))
    goal = result.scalars().first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
        
    await db.delete(goal)
    await db.commit()
    return {"message": "Goal deleted"}

@router.get("/analytics")
async def get_goal_analytics(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    result = await db.execute(select(Goal).where(Goal.user_id == uid))
    goals = result.scalars().all()
    
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.status == "completed"])
    total_target_reduction = sum(g.target_reduction for g in goals)
    total_current_progress = sum(g.current_progress for g in goals)
    
    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "total_target_reduction": total_target_reduction,
        "total_current_progress": total_current_progress,
        "overall_progress_percent": (total_current_progress / total_target_reduction * 100) if total_target_reduction > 0 else 0
    }
