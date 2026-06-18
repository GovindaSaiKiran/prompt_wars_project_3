# purpose: Provider-agnostic AI Gateway | enforces: Quality-first
from .providers.gemini import stream_gemini_response, generate_gemini_response
from typing import AsyncGenerator

class AIGateway:
    async def stream_coach_response(self, prompt: str) -> AsyncGenerator[str, None]:
        async for chunk in stream_gemini_response(prompt):
            yield chunk

    async def generate_coach_response(self, prompt: str) -> dict:
        return await generate_gemini_response(prompt)

gateway = AIGateway()
