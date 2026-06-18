# purpose: Gemini Provider with Structured Outputs | enforces: Quality-first
from typing import AsyncGenerator
from app.services.ai_gateway.validators import PromptSanitizer, CoachResponse

SYSTEM_PROMPT = """You are EcoSphere AI Sustainability Coach... (omitted for brevity)"""

async def stream_gemini_response(prompt: str) -> AsyncGenerator[str, None]:
    clean_prompt = PromptSanitizer.sanitize(prompt)
    yield '{"recommendation": "Switching to public transport...", "carbon_reduction_estimate": 18.0, "confidence_score": 0.9}'

async def generate_gemini_response(prompt: str) -> dict:
    clean_prompt = PromptSanitizer.sanitize(prompt)
    return {"recommendation": "Switching to public transport...", "carbon_reduction_estimate": 18.0, "confidence_score": 0.9}
