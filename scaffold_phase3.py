import os

def write_file(path, content):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1.1 DATA_SOURCES.md
write_file("DATA_SOURCES.md", """# purpose: Emission Factors Documentation | enforces: Quality-first, Transparency

| Source Organization | Region Coverage | Factor Type | Update Strategy | Assumptions |
|---|---|---|---|---|
| EPA | USA | Transport, Energy | Annual Sync | Average fleet MPG used for generic passenger vehicles |
| DEFRA | UK/Europe | Transport, Energy | Annual Sync | Includes well-to-tank (WTT) emissions |
| IPCC | Global | Diet, Agriculture | Bi-annual | Life-cycle analysis (LCA) boundary conditions |
""")

# 1.2 Explainable AI (Validators & Gemini)
write_file("backend/app/services/ai_gateway/validators.py", """# purpose: Prompt Sanitization & Output Validation | enforces: Security-first, Quality-first
import re
from pydantic import BaseModel, Field

class PromptSanitizer:
    @staticmethod
    def sanitize(prompt: str) -> str:
        sanitized = re.sub(r'(?i)(ignore previous instructions|system prompt|bypass)', '', prompt)
        return sanitized.strip()

class CoachResponse(BaseModel):
    recommendation: str = Field(..., description="Actionable eco-guidance")
    carbon_reduction_estimate: float = Field(..., description="Estimated kg CO2e reduced")
    confidence_score: float = Field(..., description="Confidence from 0.0 to 1.0")
    reasoning: str = Field(..., description="Explainable AI reasoning for recommendation")
    data_assumptions: str = Field(..., description="Assumptions made about user data")
""")

# 2. Sustainability Score Engine
write_file("backend/app/services/scoring/score.py", """# purpose: Sustainability Score | enforces: Quality-first
class ScoreEngine:
    @staticmethod
    def calculate_base_score(carbon_footprint: float) -> int:
        return max(0, 1000 - int(carbon_footprint * 2))
""")

write_file("backend/app/services/scoring/challenges.py", """# purpose: Challenge Logic | enforces: Quality-first
class ChallengeEngine:
    @staticmethod
    def get_bonus_points(challenge_id: str) -> int:
        return 50
""")

write_file("backend/app/services/scoring/leaderboard_contribution.py", """# purpose: Leaderboard Prep | enforces: Quality-first, Security-first
import hashlib

class LeaderboardPrep:
    @staticmethod
    def export_score(user_id: str, score: int) -> dict:
        anti_gaming_hash = hashlib.sha256(f"{user_id}:{score}:SECRET".encode()).hexdigest()
        return {"user_id": user_id, "score": score, "hash": anti_gaming_hash}
""")

# 3. Benchmarking Completion & Validation
write_file("backend/app/services/carbon_intelligence/benchmarking.py", """# purpose: Regional Benchmarks | enforces: Quality-first
class BenchmarkingService:
    @staticmethod
    def get_percentile(co2e_kg: float, region: str = "global") -> float:
        baselines = {"NA": 1500.0, "EU": 800.0, "global": 1000.0}
        baseline = baselines.get(region, baselines["global"])
        if co2e_kg <= 0: return 99.9
        percentile = max(1.0, 100.0 - ((co2e_kg / baseline) * 50.0))
        return min(percentile, 99.9)
""")

write_file("backend/tests/services/test_calculator.py", """# purpose: Edge-Case Calculation Tests | enforces: Test-first, Quality-first
import pytest
from app.services.carbon_intelligence.calculator import CarbonCalculator

def test_negative_values():
    assert CarbonCalculator.calculate("transport", -50) == 0.0

def test_extreme_values():
    assert CarbonCalculator.calculate("transport", 999999) > 0.0

def test_malformed_activity():
    assert CarbonCalculator.calculate("invalid_type", 100) == 0.0

def test_unsupported_region_fallback():
    from app.services.carbon_intelligence.benchmarking import BenchmarkingService
    assert BenchmarkingService.get_percentile(500, "UNKNOWN") == BenchmarkingService.get_percentile(500, "global")
""")

# 4. Phase 3 Backend APIs
write_file("backend/app/api/endpoints/twin.py", """# purpose: Eco Twin Router | enforces: Quality-first
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TwinScenario(BaseModel):
    variables: dict

@router.post("/simulate")
async def simulate_twin(scenario: TwinScenario):
    return {"simulated_co2e": 500.0, "difference": -150.0}
""")

write_file("backend/app/api/endpoints/planner.py", """# purpose: Sustainability Planner Router | enforces: Quality-first
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Goal(BaseModel):
    title: str
    target_reduction: float

@router.post("/")
async def create_goal(goal: Goal):
    return {"id": "123", "status": "active"}
""")

# Register routers in main.py
with open("backend/app/main.py", "r", encoding="utf-8") as f:
    main_py = f.read()

if "from app.api.endpoints.twin import router as twin_router" not in main_py:
    main_py += "\nfrom app.api.endpoints.twin import router as twin_router\napp.include_router(twin_router, prefix=\"/api/v1/twin\", tags=[\"twin\"])\n"
    main_py += "from app.api.endpoints.planner import router as planner_router\napp.include_router(planner_router, prefix=\"/api/v1/planner\", tags=[\"planner\"])\n"
    write_file("backend/app/main.py", main_py)

# 5. Phase 3 Frontend Modules
write_file("frontend/src/features/eco-twin/EcoTwinDashboard.tsx", """// purpose: Eco Twin Viz | enforces: Accessibility-first
import React from 'react';

export const EcoTwinDashboard: React.FC = () => {
  return (
    <div role="region" aria-label="Eco Twin Dashboard">
      <h2>Your Eco Twin</h2>
      <p>Current Footprint: 1000 kg CO2e</p>
    </div>
  );
};
""")

write_file("frontend/src/features/eco-twin/ScenarioBuilder.tsx", """// purpose: What-If Builder | enforces: Accessibility-first
import React from 'react';

export const ScenarioBuilder: React.FC = () => {
  return (
    <div role="region" aria-label="Scenario Builder">
      <h3>Test Scenarios</h3>
      <button>Simulate Vegan Diet</button>
    </div>
  );
};
""")

write_file("frontend/src/features/planner/GoalTracker.tsx", """// purpose: Goal Tracker UI | enforces: Accessibility-first
import React from 'react';

export const GoalTracker: React.FC = () => {
  return (
    <div role="region" aria-label="Sustainability Goals">
      <h2>Your Goals</h2>
      <ul>
        <li>Reduce Energy 10% - <progress value="50" max="100"></progress></li>
      </ul>
    </div>
  );
};
""")

print("Phase 3 scaffolding completed.")
