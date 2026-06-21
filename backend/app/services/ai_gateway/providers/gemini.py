# purpose: Gemini Provider with Structured Outputs | enforces: Quality-first
import json
import google.generativeai as genai
from typing import AsyncGenerator, Dict, Any, List
from app.services.ai_gateway.validators import PromptSanitizer
from app.core.config import settings

genai.configure(api_key=settings.gemini_api_key)

SYSTEM_PROMPT = """You are EcoSphere AI Sustainability Coach. 
Analyze the user's request regarding carbon emissions and sustainability.
Provide a JSON response with exactly four fields:
1. "recommendation": A detailed, actionable recommendation string.
2. "reasoning": The reasoning behind your recommendation.
3. "carbon_reduction_estimate": A float representing estimated kg CO2e saved.
4. "confidence_score": A float between 0.0 and 1.0 representing your confidence.

Do not wrap the JSON in markdown code blocks. Just output raw JSON.
"""

ROUTINE_PROMPT = """You are an AI that extracts carbon impact from a natural language daily routine.
Given the text, provide a JSON response with the following exact schema:
{
  "estimatedCarbonKg": float,
  "transportImpact": float,
  "electricityImpact": float,
  "foodImpact": float,
  "otherImpact": float,
  "recommendations": ["list of strings"],
  "ecoScore": float
}
Do not wrap the JSON in markdown code blocks. Just output raw JSON.
"""

# We'll use Gemini 2.5 Flash for faster responses
model = genai.GenerativeModel('gemini-2.5-flash')

def build_context_prompt(base_prompt: str, context: Dict[str, Any] = None, history: List[Dict[str, str]] = None) -> str:
    prompt_parts = [SYSTEM_PROMPT]
    
    if context:
        prompt_parts.append(f"\nContext Data:\n{json.dumps(context, indent=2)}")
        
    if history:
        prompt_parts.append("\nRecent Conversation History:")
        for msg in history:
            prompt_parts.append(f"{msg['role'].capitalize()}: {msg['content']}")
            
    prompt_parts.append(f"\nUser Request: {base_prompt}")
    return "\n".join(prompt_parts)

async def stream_gemini_response(prompt: str, context: Dict[str, Any] = None, history: List[Dict[str, str]] = None) -> AsyncGenerator[str, None]:
    clean_prompt = PromptSanitizer.sanitize(prompt)
    full_prompt = build_context_prompt(clean_prompt, context, history)
    try:
        response = await model.generate_content_async(full_prompt, stream=True)
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield json.dumps({
            "recommendation": f"Error contacting AI Coach: {str(e)}",
            "reasoning": "Error",
            "carbon_reduction_estimate": 0.0,
            "confidence_score": 0.0
        })

async def generate_gemini_response(prompt: str, context: Dict[str, Any] = None, history: List[Dict[str, str]] = None) -> dict:
    clean_prompt = PromptSanitizer.sanitize(prompt)
    full_prompt = build_context_prompt(clean_prompt, context, history)
    try:
        response = await model.generate_content_async(full_prompt)
        text = response.text
        # Strip potential markdown formatting if model didn't obey
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {
            "recommendation": f"Error: {str(e)}",
            "reasoning": "Error",
            "carbon_reduction_estimate": 0.0,
            "confidence_score": 0.0
        }

async def analyze_routine_with_gemini(routine_text: str) -> dict:
    clean_text = PromptSanitizer.sanitize(routine_text)
    full_prompt = f"{ROUTINE_PROMPT}\n\nUser Routine: {clean_text}"
    try:
        response = await model.generate_content_async(full_prompt)
        text = response.text
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        raise Exception(f"Failed to analyze routine: {e}")

