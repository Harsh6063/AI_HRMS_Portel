import os

from groq import Groq

from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv(
    "GROQ_API_KEY"
)

if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY not found"
    )

client = Groq(
    api_key=groq_api_key
)

# =========================
# GENERATE AI SUMMARY
# =========================

def generate_ai_summary(
    resume_text: str,
    role: str
):
    prompt = f"""
    Analyze this resume for a {role} role.

    Give response in this format:

    Professional Summary:
    <summary>

    Key Strengths:
    - point
    - point

    Missing Skills / Concerns:
    - point
    - point

    Communication Assessment:
    <assessment>

    Hiring Recommendation:
    <recommendation>

    Resume:
    {resume_text[:12000]}
    """

    response = (
        client.chat.completions.create(
            model=
                "llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",

                    "content": prompt
                }
            ],

            temperature=0.4
        )
    )

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
    )