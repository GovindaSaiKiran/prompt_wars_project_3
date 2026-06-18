# purpose: Report Generator | enforces: Quality-first
from typing import List

class ReportGenerator:
    @staticmethod
    def generate_monthly_report(user_id: str, calculations: List[dict], goals: List[dict]) -> dict:
        total_co2e = sum(c.get('co2e_kg', 0) for c in calculations)
        goals_completed = len([g for g in goals if g.get('status') == 'completed'])
        return {
            "summary": f"You generated {total_co2e} kg CO2e this month and completed {goals_completed} goals.",
            "metrics": {"total_co2e": total_co2e, "goals_completed": goals_completed}
        }
