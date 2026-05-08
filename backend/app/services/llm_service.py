from openai import OpenAI
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# Load environment variables
# ─────────────────────────────────────────────
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ─────────────────────────────────────────────
# STRICT DETAIL CONFIG (ENFORCED OUTPUT)
# ─────────────────────────────────────────────
DETAIL_CONFIG = {
    "Brief": {
        "instruction": (
            "STRICTLY follow:\n"
            "- Output ONLY bullet points\n"
            "- EXACTLY 5 to 7 bullets (no more, no less)\n"
            "- Each bullet MUST be one short sentence (max 12 words)\n"
            "- No paragraphs\n"
            "- No explanations\n"
        ),
    },
    "Standard": {
        "instruction": (
            "STRICTLY follow:\n"
            "- Output exactly 2 paragraphs\n"
            "- Each paragraph should have 4–6 lines\n"
            "- Cover all key ideas clearly\n"
            "- No bullet points\n"
        ),
    },
    "Thorough": {
        "instruction": (
            "STRICTLY follow this structure:\n\n"
            "1. Overview (6–8 lines)\n"
            "2. Key Points (8–12 bullet points)\n"
            "3. Detailed Insights (10–15 lines)\n"
            "4. Implications / Recommendations (5–8 points)\n"
            "5. Conclusion (4–6 lines)\n\n"
            "Do NOT skip any section.\n"
            "Make it detailed and significantly longer than other modes."
        ),
    },
}


# ─────────────────────────────────────────────
# SAFE RESPONSE EXTRACTION
# ─────────────────────────────────────────────
def extract_text(response):
    try:
        return response.output[0].content[0].text.strip()
    except Exception:
        return str(response)


# ─────────────────────────────────────────────
# MAIN SUMMARIZATION FUNCTION
# ─────────────────────────────────────────────
def summarize_text(text: str, detail_level: str = "Standard") -> str:

    if detail_level not in DETAIL_CONFIG:
        detail_level = "Standard"

    instruction = DETAIL_CONFIG[detail_level]["instruction"]

    # 🔥 truncate (safe limit)
    truncated_text = text[:15000]

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict document summarizer.\n"
                        "You MUST follow formatting instructions exactly.\n"
                        "Do NOT ignore bullet counts, paragraph limits, or structure.\n"
                        "If instructions say EXACT numbers, follow them strictly.\n"
                        "Never say 'not found'. Always produce a structured summary."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
{instruction}

IMPORTANT:
- Follow the format EXACTLY
- If format is violated, correct it before answering
- Ensure output length matches the requested detail level

Document:
{truncated_text}
"""
                }
            ]
        )

        return extract_text(response)

    except Exception as e:
        return f"Error: {str(e)}"