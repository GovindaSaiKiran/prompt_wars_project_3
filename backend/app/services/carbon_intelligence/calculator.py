# purpose: Calculate CO2e | enforces: Quality-first
from .emission_factors import EmissionFactors

class CarbonCalculator:
    @staticmethod
    def calculate(activity_type: str, value: float) -> float:
        factor = EmissionFactors.get_factor(activity_type)
        return factor * value
