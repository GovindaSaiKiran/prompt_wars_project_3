# purpose: Load Emission Factors | enforces: Quality-first
import json
import os

class EmissionFactors:
    @staticmethod
    def get_factor(activity_type: str) -> float:
        # Dummy lookup logic
        factors = {
            'transport': 0.2, # kg CO2e per km
            'energy': 0.4,    # kg CO2e per kWh
            'diet': 2.5       # kg CO2e per meal
        }
        return factors.get(activity_type, 0.0)
