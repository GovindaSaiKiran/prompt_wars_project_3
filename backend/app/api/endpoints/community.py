from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from pydantic import BaseModel
import uuid

from app.db.session import get_db
from app.models.community import CommunityPost
from app.core.auth import verify_firebase_token

router = APIRouter()

class PostCreate(BaseModel):
    content: str
    username: str

class PostResponse(BaseModel):
    id: str
    user_id: str
    username: str
    content: str
    likes: int
    created_at: str

@router.get("/", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CommunityPost).order_by(desc(CommunityPost.created_at)).limit(50)
    )
    posts = result.scalars().all()
    return [
        PostResponse(
            id=p.id,
            user_id=p.user_id,
            username=p.username,
            content=p.content,
            likes=p.likes,
            created_at=p.created_at.isoformat() if p.created_at else ""
        ) for p in posts
    ]

@router.post("/", response_model=PostResponse)
async def create_post(
    req: PostCreate,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    post_id = str(uuid.uuid4())
    post = CommunityPost(
        id=post_id,
        user_id=uid,
        username=req.username,
        content=req.content,
        likes=0
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    
    return PostResponse(
        id=post.id,
        user_id=post.user_id,
        username=post.username,
        content=post.content,
        likes=post.likes,
        created_at=post.created_at.isoformat() if post.created_at else ""
    )
