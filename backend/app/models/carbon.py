from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base

class CarbonEntry(Base):
    __tablename__ = "carbon_entries"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False) # Maps to Firebase UID
    category = Column(String, nullable=False)
    activity = Column(String, nullable=False, server_default="unknown")
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    carbon_calculated = Column(Float, nullable=False)
    source_reference = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
