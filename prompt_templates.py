from typing import List

SYSTEM_GREETING = """You are TalentScout, an AI hiring assistant for a tech recruitment agency.
Your tasks:
1) Greet, set expectations (~10 minutes), and collect details.
2) Ask only one question at a time.
3) Keep tone professional, concise, warm.
4) Obey end keywords: ['quit','exit','stop','end','goodbye'] -> conclude politely.
5) Never collect sensitive data beyond: name, email, phone, years of experience, desired positions, location, tech stack.
6) If confused, ask a brief clarifying question."""

def qgen_prompt(tech_stack: List[str]) -> str:
    return f"""
Generate 3-5 practical, screening-level technical questions for EACH of: {', '.join(tech_stack)}.
Rules:
- Prefer scenario-based and implementation-focused questions.
- Mix difficulty (basic/intermediate).
- Avoid trivia-only questions.
- Output JSON: {"technology": [{"q": "..."}, ...]} aggregated across all techs.
"""

def validate_field_prompt(field_name: str, value: str) -> str:
    return f"""
Validate candidate {field_name} for format and reasonableness.
Value: {value}
Return STRICT JSON: {"valid": true|false, "reason": "short reason", "normalized": "cleaned value or ''"}.
"""

SUMMARY_PROMPT = """
Produce a short, recruiter-friendly summary (3-5 bullets) of the candidate's profile using provided fields.
Focus on tech strengths, experience highlights, target roles, and location readiness.
Return plain text bullets.
"""