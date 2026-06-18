# purpose: Edge-Case Calculation Tests | enforces: Test-first, Quality-first
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
