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
    assert isinstance(CarbonCalculator.calculate("electricity", 100.0), float)
    assert isinstance(EmissionFactors.get_factor("electricity"), float)
    assert isinstance(BenchmarkingService.get_percentile(500.0), float)

def test_scoring_engine():
    assert isinstance(ScoreEngine.calculate_base_score(500.0), int)
    res = LeaderboardPrep.export_score("user1", 100)
    assert "hash" in res
    assert isinstance(ChallengeEngine.get_bonus_points("challenge1"), int)

def test_reports_engine():
    assert isinstance(TrendAnalysis.analyze("user1"), dict)
    assert isinstance(ReportGenerator.generate_monthly_report("user1", [], []), dict)
    assert isinstance(PDFExport.export({}), bytes)
    assert isinstance(ImpactSummary.summarize("user1"), dict)

def test_community_validation():
    assert isinstance(RankingValidator.is_valid_score("user1", 100, "hash"), bool)
    assert isinstance(FraudDetector.is_duplicate_activity("user1", "hash"), bool)
    assert isinstance(AnomalyDetector.is_anomalous_jump(100, 110), bool)
    assert isinstance(AnomalyDetector.is_anomalous_jump(100, 1000), bool)

def test_challenges_engine():
    assert isinstance(RewardEngine.distribute_points("user1", 50), bool)
    assert isinstance(CompletionValidator.validate_proof([], {}), bool)
    assert isinstance(ChallengeManager.list_active(), list)

@pytest.mark.asyncio
async def test_ai_gateway():
    assert PromptSanitizer.sanitize("test prompt") == "test prompt"
    gateway = AIGateway()
    res = await gateway.generate_coach_response("test")
    assert "recommendation" in res
    
    chunks = [c async for c in gateway.stream_coach_response("test")]
    assert len(chunks) > 0

def test_endpoints():
    res = client.post("/api/v1/carbon/calculate", json={"activityType": "electricity", "value": 100, "unit": "kWh"})
    assert res.status_code == 200
    res = client.post("/api/v1/planner/", json={"title": "Save Energy", "target_reduction": 50})
    assert res.status_code == 200
    res = client.post("/api/v1/twin/simulate", json={"variables": {}})
    assert res.status_code == 200
    res = client.post("/api/v1/coach/chat", json={"message": "hello"})
    assert res.status_code == 200
    res = client.get("/api/v1/community/leaderboard")
    assert res.status_code == 200
    res = client.post("/api/v1/community/impact", json={"user_id": "test", "score": 10})
    assert res.status_code == 200
