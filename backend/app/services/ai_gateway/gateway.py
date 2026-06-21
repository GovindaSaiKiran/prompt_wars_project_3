# purpose: Provider-agnostic AI Gateway | enforces: Quality-first
from .providers.gemini import stream_gemini_response, generate_gemini_response, analyze_routine_with_gemini
from typing import AsyncGenerator, Dict, Any, List

class AIGateway:
    async def stream_coach_response(self, prompt: str, context: Dict[str, Any] = None, history: List[Dict[str, str]] = None) -> AsyncGenerator[str, None]:
        async for chunk in stream_gemini_response(prompt, context, history):
            yield chunk

    async def generate_coach_response(self, prompt: str, context: Dict[str, Any] = None, history: List[Dict[str, str]] = None) -> dict:
        return await generate_gemini_response(prompt, context, history)

    async def analyze_routine(self, text: str) -> dict:
        return await analyze_routine_with_gemini(text)

gateway = AIGateway()
