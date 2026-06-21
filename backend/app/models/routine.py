from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class RoutineAnalysis(Base):
    __tablename__ = "routine_analyses"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False) # Maps to Firebase UID
    original_text = Column(Text, nullable=False)
    estimated_carbon_kg = Column(Float, nullable=False)
    transport_impact = Column(Float, nullable=False)
    electricity_impact = Column(Float, nullable=False)
    food_impact = Column(Float, nullable=False)
    other_impact = Column(Float, nullable=False)
    eco_score = Column(Float, nullable=False)
    recommendations = Column(Text) # JSON string of recommendations
    created_at = Column(DateTime(timezone=True), server_default=func.now())
