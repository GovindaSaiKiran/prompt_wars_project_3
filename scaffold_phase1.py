import os

def write_file(path, content):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. Shared Models
write_file("packages/shared/models/coach-message.ts", """// purpose: AI Coach Message Schema | enforces: Quality-first
import { z } from 'zod';

export const CoachMessageSchema = z.object({
  id: z.string(),
  role: z.enum(['user', 'model']),
  content: z.string(),
  timestamp: z.number(),
});

export type CoachMessage = z.infer<typeof CoachMessageSchema>;
""")

write_file("packages/shared/models/ai-conversation.ts", """// purpose: AI Conversation Schema | enforces: Quality-first
import { z } from 'zod';
import { CoachMessageSchema } from './coach-message';

export const AiConversationSchema = z.object({
  id: z.string(),
  userId: z.string(),
  title: z.string(),
  messages: z.array(CoachMessageSchema),
  createdAt: z.number(),
  updatedAt: z.number(),
  metadata: z.record(z.string(), z.any()).optional(),
});

export type AiConversation = z.infer<typeof AiConversationSchema>;
""")

# 2. Firestore Rules Update
with open("infra/firebase/firestore.rules", "r", encoding="utf-8") as f:
    rules = f.read()

new_rules = rules.replace(
    "match /{document=**} {\n      allow read, write: if false; // Deny by default\n    }",
    """match /{document=**} {
      allow read, write: if false; // Deny by default
    }
    match /users/{userId}/ai_conversations/{conversationId} {
      allow read, write, delete: if request.auth != null && request.auth.uid == userId;
    }"""
)
write_file("infra/firebase/firestore.rules", new_rules)

# 3. Backend Implementation
write_file("backend/app/services/ai_gateway/providers/gemini.py", '''# purpose: Gemini Provider | enforces: Quality-first
from typing import AsyncGenerator

SYSTEM_PROMPT = """You are EcoSphere AI Sustainability Coach.
Your goal is to help users make practical sustainability improvements.
Always:
* Provide evidence-based recommendations.
* Explain environmental impact clearly.
* Quantify carbon reductions when possible.
* Suggest realistic actions.
* Prioritize high-impact changes.
* Be encouraging and supportive.

Never:
* Shame users.
* Exaggerate environmental benefits.
* Provide unsafe advice.
* Invent sustainability statistics.

When data is uncertain:
* State assumptions clearly.
* Provide estimates instead of definitive claims.

Responses should focus on:
* Carbon reduction
* Cost savings
* Sustainability score improvement
* Long-term environmental impact
* User-specific circumstances"""

async def stream_gemini_response(prompt: str) -> AsyncGenerator[str, None]:
    # Dummy streaming generator
    yield '{"text": "Switching from private vehicles to public transport twice a week"}'
    yield '{"text": " could reduce your monthly emissions by approximately 18 kg CO₂"}'
    yield '{"text": " while also reducing transportation costs."}'

async def generate_gemini_response(prompt: str) -> dict:
    return {"text": "Switching from private vehicles to public transport twice a week could reduce your monthly emissions by approximately 18 kg CO₂ while also reducing transportation costs."}
''')

write_file("backend/app/services/ai_gateway/gateway.py", """# purpose: Provider-agnostic AI Gateway | enforces: Quality-first
from .providers.gemini import stream_gemini_response, generate_gemini_response
from typing import AsyncGenerator

class AIGateway:
    async def stream_coach_response(self, prompt: str) -> AsyncGenerator[str, None]:
        async for chunk in stream_gemini_response(prompt):
            yield chunk

    async def generate_coach_response(self, prompt: str) -> dict:
        return await generate_gemini_response(prompt)

gateway = AIGateway()
""")

write_file("backend/app/api/endpoints/coach.py", """# purpose: AI Coach Router | enforces: Security-first
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.services.ai_gateway.gateway import gateway
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(gateway.stream_coach_response(request.message), media_type="text/event-stream")

@router.post("/chat")
async def chat(request: ChatRequest):
    return await gateway.generate_coach_response(request.message)
""")

# Register router in main.py
with open("backend/app/main.py", "r", encoding="utf-8") as f:
    main_py = f.read()

if "from app.api.endpoints.coach import router as coach_router" not in main_py:
    main_py = main_py.replace(
        "app = FastAPI()",
        "app = FastAPI()\n\nfrom app.api.endpoints.coach import router as coach_router\napp.include_router(coach_router, prefix=\"/api/v1/coach\", tags=[\"coach\"])"
    )
    write_file("backend/app/main.py", main_py)

print("Phase 1 scaffolding completed.")
