from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    username = Column(String, nullable=False)
    content = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
