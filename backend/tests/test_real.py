import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.services.scoring.score import ScoringEngine
from app.services.scoring.leaderboard_contribution import LeaderboardService
from app.services.scoring.challenges import ChallengeScoring
from app.services.reports.trend_analysis import TrendAnalyzer
from app.services.reports.report_generator import ReportGenerator
from app.services.reports.pdf_export import PDFExporter
from app.services.reports.impact_summary import ImpactSummarizer
from app.services.community.ranking_validator import RankingValidator
from app.services.community.fraud_detection import FraudDetector
from app.services.community.anomaly_detection import AnomalyDetector
from app.services.challenges.reward_engine import RewardEngine
from app.services.challenges.completion_validator import CompletionValidator
from app.services.challenges.challenge_manager import ChallengeManager
from app.services.carbon_intelligence.emission_factors import EmissionFactorDB
from app.services.carbon_intelligence.calculator import CarbonCalculator
from app.services.carbon_intelligence.benchmarking import BenchmarkingEngine
from app.services.ai_gateway.validators import PromptValidator
from app.services.ai_gateway.gateway import AIGateway

client = TestClient(app)

def test_carbon_calculator():
    assert CarbonCalculator.calculate("electricity", 100.0) == 45.0
    assert EmissionFactorDB.get_factor("electricity") == 0.45
    assert BenchmarkingEngine.get_percentile(500.0) == 85.0

def test_scoring_engine():
    assert ScoringEngine.calculate_base_score(500.0) == 85
    assert LeaderboardService.export_score("user1", 100) == {"user_id": "user1", "score": 100}
    assert ChallengeScoring.get_bonus_points("challenge1") == 50

def test_reports_engine():
    assert TrendAnalyzer.analyze("user1") == {"trend": "improving"}
    assert ReportGenerator.generate_monthly_report("user1", [], []) == {"report": "generated"}
    assert PDFExporter.export({}) == b"pdf_data"
    assert ImpactSummarizer.summarize("user1") == {"impact": "high"}

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
    assert PromptValidator.sanitize("test prompt") == "test prompt"
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
