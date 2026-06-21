from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False) # Maps to Firebase UID
    title = Column(String, nullable=False)
    description = Column(String)
    goal_type = Column(String, default="daily") # daily, weekly, monthly
    target_reduction = Column(Float, nullable=False) # target kg CO2e reduction
    current_progress = Column(Float, default=0.0) # current kg CO2e reduced
    status = Column(String, default="active") # active, completed, abandoned
    deadline = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
