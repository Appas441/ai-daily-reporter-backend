from openai import OpenAI
from app.utils.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def format_logs(logs):
    if not logs:
        return "No work updates provided today."

    combined_logs = "\n".join([f"- {log}" for log in logs])

    prompt = f"""
Write a professional end-of-day email.

Rules:
- Start with greeting (Hi Sir,)
- Convert work into bullet points
- Keep it short and clear
- End with: Regards, Appas

Work Done:
{combined_logs}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content