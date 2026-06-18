# purpose: App entrypoint | enforces: Quality-first
from fastapi import FastAPI
from app.core.security import add_security_headers

app = FastAPI()

from app.api.endpoints.coach import router as coach_router
app.include_router(coach_router, prefix="/api/v1/coach", tags=["coach"])
from app.api.endpoints.carbon import router as carbon_router
app.include_router(carbon_router, prefix="/api/v1/carbon", tags=["carbon"])

@app.middleware("http")
async def add_security_headers_middleware(request, call_next):
    response = await call_next(request)
    return add_security_headers(response)

@app.get("/health")
def health_check():
    return {"status": "ok"}

from app.api.endpoints.twin import router as twin_router
app.include_router(twin_router, prefix="/api/v1/twin", tags=["twin"])
from app.api.endpoints.planner import router as planner_router
app.include_router(planner_router, prefix="/api/v1/planner", tags=["planner"])
from app.api.endpoints.community import router as community_router
app.include_router(community_router, prefix="/api/v1/community", tags=["community"])
