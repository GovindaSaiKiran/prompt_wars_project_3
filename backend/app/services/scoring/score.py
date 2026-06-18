# purpose: Sustainability Score | enforces: Quality-first
class ScoreEngine:
    @staticmethod
    def calculate_base_score(carbon_footprint: float) -> int:
        return max(0, 1000 - int(carbon_footprint * 2))
