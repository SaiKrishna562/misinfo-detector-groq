import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def analyse_claim(claim: str, sources: list) -> dict:
    sources_text = "\n".join([
        f"- [{s['title']}] ({s['url']}): {s['snippet']}"
        for s in sources if s.get("snippet")
    ])

    prompt = f"""You are a professional fact-checker. Your job is to verify whether the claim below is TRUE, FALSE, MISLEADING, or UNVERIFIED.

Claim to verify: {claim}

Sources found:
{sources_text}

CRITICAL RULES:
- Evaluate the claim EXACTLY as written — do NOT flip or negate it
- If the claim says "lightning never strikes the same place twice", check if THAT statement is true or false
- If the claim is a myth or false belief, the verdict should be FALSE or MISLEADING — NOT TRUE
- A low score means the claim itself is not credible/accurate
- A high score means the claim itself is well-supported and accurate

Score the claim using this STRICT rubric:
- 85-100 : Claim is TRUE — multiple credible sources confirm it
- 65-84  : Claim is mostly TRUE — minor details disputed
- 45-64  : Mixed evidence — cannot confirm or deny clearly
- 25-44  : Claim is mostly FALSE — mostly contradicted or misleading framing
- 0-24   : Claim is clearly FALSE — debunked by multiple credible sources

Verdict rules:
- TRUE        => score 65-100, sources confirm the claim as stated
- FALSE       => score 0-35,   sources contradict the claim as stated
- MISLEADING  => score 25-64,  claim has partial truth but misleading framing
- UNVERIFIED  => score 40-60,  insufficient sources to confirm or deny

Return ONLY a valid JSON object. No markdown, no extra text.

{{
  "verdict": "TRUE|FALSE|MISLEADING|UNVERIFIED",
  "score": <integer 0-100>,
  "reasoning": "<2-3 sentences explaining why the claim as written is true/false/misleading>",
  "key_finding": "<one sentence max 12 words — what the evidence actually shows>",
  "supporting_sources": ["<url of source that supports the claim AS WRITTEN>"],
  "contradicting_sources": ["<url of source that contradicts the claim AS WRITTEN>"],
  "bias_flags": ["<e.g. common misconception, cherry-picked data, misleading headline>"]
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=900,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "verdict": "UNVERIFIED",
            "score": 50,
            "reasoning": "Could not parse the analysis response. Please try again.",
            "key_finding": "Analysis unavailable — please retry",
            "supporting_sources": [],
            "contradicting_sources": [],
            "bias_flags": []
        }
