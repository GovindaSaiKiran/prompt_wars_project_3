from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class EmissionFactor(Base):
    __tablename__ = "emission_factors"

    id = Column(String, primary_key=True, index=True)
    category = Column(String, index=True, nullable=False) # e.g., 'transport', 'energy', 'food'
    activity = Column(String, nullable=False) # e.g., 'driving_gasoline_car'
    factor = Column(Float, nullable=False) # e.g., 0.411 (kg CO2e per unit)
    unit = Column(String, nullable=False) # e.g., 'miles'
    source = Column(String, nullable=False) # e.g., 'EPA 2023'
    region = Column(String, default="Global")
    cost_per_unit = Column(Float, default=0.0) # Cost estimation per unit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
