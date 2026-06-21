from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, unique=True)
    username = Column(String, nullable=False)
    score = Column(Float, default=0.0)
    reduction_pct = Column(Float, default=0.0)
    streak = Column(Integer, default=0)
    region = Column(String, default="Global")
    emoji = Column(String, default="🌱")
    signature = Column(String, nullable=False) # HMAC signature to prove authenticity
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
