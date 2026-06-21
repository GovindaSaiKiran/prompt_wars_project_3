from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
import firebase_admin
from firebase_admin import auth
import google.generativeai as genai
from app.core.config import settings
import time

router = APIRouter()

@router.get("/db-health")
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        start_time = time.time()
        await db.execute(text("SELECT 1"))
        latency = (time.time() - start_time) * 1000
        return {"connected": True, "latencyMs": round(latency, 2)}
    except Exception as e:
        return {"connected": False, "error": str(e)}

@router.get("/gemini-health")
async def gemini_health():
    try:
        start_time = time.time()
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Lightweight check
        response = model.generate_content("Ping")
        latency = (time.time() - start_time) * 1000
        return {
            "connected": True,
            "model": "gemini-1.5-flash",
            "lastSuccessfulCall": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "latencyMs": round(latency, 2)
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}

@router.get("/auth-health")
async def auth_health():
    try:
        app = firebase_admin.get_app()
        if app:
            return {"connected": True, "project_id": settings.firebase_project_id}
    except Exception as e:
        return {"connected": False, "error": str(e)}
