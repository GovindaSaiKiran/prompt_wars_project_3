from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class CalculatorEntry(Base):
    __tablename__ = "calculator_entries"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False) # Maps to Firebase UID
    distance = Column(Float, nullable=False)
    vehicle_type = Column(String, nullable=False)
    carbon_produced_kg = Column(Float, nullable=False)
    money_spent = Column(Float, nullable=False)
    eco_alternative_savings_kg = Column(Float, nullable=False)
    eco_alternative_savings_money = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
