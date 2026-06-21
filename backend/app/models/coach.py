from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False) # Maps to Firebase UID
    role = Column(String, nullable=False) # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
