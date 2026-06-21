# purpose: App entrypoint | enforces: Quality-first
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.security import add_security_headers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import firebase_admin
from firebase_admin import credentials
from app.core.config import settings

try:
    if not firebase_admin._apps:
        # We'll use actual credentials
        firebase_admin.initialize_app(options={'projectId': settings.firebase_project_id})
except Exception as e:
    import traceback
    print(f"Failed to initialize Firebase: {e}")
    traceback.print_exc()

from fastapi.responses import RedirectResponse

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

from app.api.endpoints.coach import router as coach_router
app.include_router(coach_router, prefix="/api/v1/coach", tags=["coach"])
from app.api.endpoints.carbon import router as carbon_router
app.include_router(carbon_router, prefix="/api/v1/carbon", tags=["carbon"])

@app.middleware("http")
async def add_security_headers_middleware(request, call_next):
    response = await call_next(request)
    return add_security_headers(response)

from app.api.endpoints import system
app.include_router(system.router, prefix="/api/v1/system", tags=["System"])

from app.api.endpoints import auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

from app.api.endpoints.twin import router as twin_router
app.include_router(twin_router, prefix="/api/v1/twin", tags=["twin"])
from app.api.endpoints.planner import router as planner_router
app.include_router(planner_router, prefix="/api/v1/planner", tags=["planner"])
from app.api.endpoints.community import router as community_router
app.include_router(community_router, prefix="/api/v1/community", tags=["community"])
from app.api.endpoints.leaderboard import router as leaderboard_router
app.include_router(leaderboard_router, prefix="/api/v1/leaderboard", tags=["leaderboard"])
from app.api.endpoints.reports import router as reports_router
app.include_router(reports_router, prefix="/api/v1/reports", tags=["reports"])

from app.api.endpoints.calculator import router as calculator_router
app.include_router(calculator_router, prefix="/api/v1/calculator", tags=["calculator"])

from app.api.endpoints.routine import router as routine_router
app.include_router(routine_router, prefix="/api/v1/routine-analyzer", tags=["routine"])

from app.api.endpoints.analytics import router as analytics_router
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["analytics"])
