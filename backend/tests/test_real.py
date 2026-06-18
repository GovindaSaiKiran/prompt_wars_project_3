import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.services.scoring.score import ScoreEngine
from app.services.scoring.leaderboard_contribution import LeaderboardPrep
from app.services.scoring.challenges import ChallengeEngine
from app.services.reports.trend_analysis import TrendAnalysis
from app.services.reports.report_generator import ReportGenerator
from app.services.reports.pdf_export import PDFExport
from app.services.reports.impact_summary import ImpactSummary
from app.services.community.ranking_validator import RankingValidator
from app.services.community.fraud_detection import FraudDetector
from app.services.community.anomaly_detection import AnomalyDetector
from app.services.challenges.reward_engine import RewardEngine
from app.services.challenges.completion_validator import CompletionValidator
from app.services.challenges.challenge_manager import ChallengeManager
from app.services.carbon_intelligence.emission_factors import EmissionFactors
from app.services.carbon_intelligence.calculator import CarbonCalculator
from app.services.carbon_intelligence.benchmarking import BenchmarkingService
from app.services.ai_gateway.validators import PromptSanitizer
from app.services.ai_gateway.gateway import AIGateway

client = TestClient(app)

def test_carbon_calculator():
    assert CarbonCalculator.calculate("electricity", 100.0) == 45.0
    assert EmissionFactors.get_factor("electricity") == 0.45
    assert BenchmarkingService.get_percentile(500.0) == 85.0

def test_scoring_engine():
    assert ScoreEngine.calculate_base_score(500.0) == 0
    assert LeaderboardPrep.export_score("user1", 100) == {"user_id": "user1", "score": 100}
    assert ChallengeEngine.get_bonus_points("challenge1") == 50

def test_reports_engine():
    assert TrendAnalysis.analyze("user1") == {"trend": "improving"}
    assert ReportGenerator.generate_monthly_report("user1", [], []) == {"report": "generated"}
    assert PDFExport.export({}) == b"pdf_data"
    assert ImpactSummary.summarize("user1") == {"impact": "high"}

def test_community_validation():
    assert RankingValidator.is_valid_score("user1", 100, "hash") == True
    assert FraudDetector.is_duplicate_activity("user1", "hash") == False
    assert AnomalyDetector.is_anomalous_jump(100, 110) == False
    assert AnomalyDetector.is_anomalous_jump(100, 1000) == True

def test_challenges_engine():
    assert RewardEngine.distribute_points("user1", 50) == True
    assert CompletionValidator.validate_proof([], {}) == True
    assert ChallengeManager.list_active() == []

@pytest.mark.asyncio
async def test_ai_gateway():
    assert PromptSanitizer.sanitize("test prompt") == "test prompt"
    gateway = AIGateway()
    res = await gateway.generate_coach_response("test")
    assert "simulated" in res["text"]
    
    # testing async generator stream
    chunks = [c async for c in gateway.stream_coach_response("test")]
    assert len(chunks) > 0

def test_endpoints():
    res = client.post("/api/v1/carbon/calculate", json={"activity_type": "electricity", "value": 100})
    assert res.status_code == 200
    res = client.post("/api/v1/planner/goals", json={"title": "Save Energy", "target_co2e_reduction": 50})
    assert res.status_code == 200
    res = client.post("/api/v1/twin/simulate", json={"variables": {}})
    assert res.status_code == 200
    res = client.post("/api/v1/coach/chat", json={"message": "hello"})
    assert res.status_code == 200
    res = client.get("/api/v1/community/leaderboard")
    assert res.status_code == 200
    res = client.post("/api/v1/community/impact", json={"user_id": "test", "score": 10})
    assert res.status_code == 200
