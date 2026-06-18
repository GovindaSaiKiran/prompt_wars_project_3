# purpose: Verify Anti-Gaming Measures | enforces: Security-first, Test-first
import pytest
from app.services.community.anomaly_detection import AnomalyDetector
from app.services.community.ranking_validator import RankingValidator
from app.services.scoring.leaderboard_contribution import LeaderboardPrep

def test_anomaly_detection_rejects_impossible_jump():
    assert AnomalyDetector.is_anomalous_jump(100, 700) == True
    assert AnomalyDetector.is_anomalous_jump(100, 150) == False

def test_ranking_validator_accepts_valid_hash():
    data = LeaderboardPrep.export_score("user_1", 850)
    assert RankingValidator.is_valid_score("user_1", 850, data["hash"]) == True

def test_ranking_validator_rejects_tampered_score():
    data = LeaderboardPrep.export_score("user_1", 850)
    assert RankingValidator.is_valid_score("user_1", 9999, data["hash"]) == False
