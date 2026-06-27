import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def extract_claims(user_input: str) -> list:
    prompt = f"""You are a fact-checking assistant. The user has submitted a statement to be fact-checked.

Your job is to extract 2-4 specific, verifiable factual claims FROM the user's original statement.

CRITICAL RULES:
- Extract claims EXACTLY as implied by the user's input — do NOT flip, negate, or reframe them
- If the user says "lightning never strikes the same place twice", extract: "Lightning never strikes the same place twice"
- If the user says "vaccines cause autism", extract: "Vaccines cause autism"
- If the user says "the earth is flat", extract: "The earth is flat"
- Preserve the original meaning and direction of the claim
- Only break into sub-claims if the input contains multiple distinct assertions

Return ONLY a valid JSON array of strings. No explanation, no markdown, no extra text.

User input: {user_input}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
