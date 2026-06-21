import google.generativeai as genai
import asyncio

genai.configure(api_key="AQ.Ab8RN6I5rj2PagkEiAubvZSBs3066YVpPt_3bKpL3kSO-6wr5g")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
