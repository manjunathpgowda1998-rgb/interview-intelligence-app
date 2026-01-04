import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def evaluate_answer(answer_text, role="CloudOps Engineer"):
    prompt = f"""
You are a senior interviewer for the role of {role}.

Analyze the following interview answer.

Answer:
{answer_text}

Return ONLY valid JSON with:
- score (0 to 10)
- strengths (list)
- weaknesses (list)
- missing_concepts (list)
- follow_up_questions (list)
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    data = response.json()

    if "response" not in data:
        print("⚠️ Raw Ollama response:")
        print(json.dumps(data, indent=2))
        raise RuntimeError("Ollama did not return expected response field")

    text = data["response"]

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "raw_output": text
        }
