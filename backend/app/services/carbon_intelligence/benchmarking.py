# purpose: Regional Benchmarks | enforces: Quality-first
class BenchmarkingService:
    @staticmethod
    def get_percentile(co2e_kg: float, region: str = "global") -> float:
        baselines = {"NA": 1500.0, "EU": 800.0, "global": 1000.0}
        baseline = baselines.get(region, baselines["global"])
        if co2e_kg <= 0: return 99.9
        percentile = max(1.0, 100.0 - ((co2e_kg / baseline) * 50.0))
        return min(percentile, 99.9)
