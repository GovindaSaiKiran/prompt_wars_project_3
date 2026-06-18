# purpose: Prompt Sanitization & Output Validation | enforces: Security-first, Quality-first
import re
from pydantic import BaseModel, Field

class PromptSanitizer:
    @staticmethod
    def sanitize(prompt: str) -> str:
        sanitized = re.sub(r'(?i)(ignore previous instructions|system prompt|bypass)', '', prompt)
        return sanitized.strip()

class CoachResponse(BaseModel):
    recommendation: str = Field(..., description="Actionable eco-guidance")
    carbon_reduction_estimate: float = Field(..., description="Estimated kg CO2e reduced")
    confidence_score: float = Field(..., description="Confidence from 0.0 to 1.0")
    reasoning: str = Field(..., description="Explainable AI reasoning for recommendation")
    data_assumptions: str = Field(..., description="Assumptions made about user data")
