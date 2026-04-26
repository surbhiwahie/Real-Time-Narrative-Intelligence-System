from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_trends(trends_text):
    prompt = f"""
You are a data intelligence analyst.

Given these narrative trends from YouTube:

{trends_text}

Explain:
1. What is happening overall
2. Which narratives are rising or falling
3. Why this matters
4. A short executive summary
5. Explain what these trends mean for media, business, or public attention.

Be concise and professional.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content