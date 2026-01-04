import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi"   # Fast CPU model

def generate_answer(question: str, role="DevOps Engineer") -> str:
    prompt = f"""
You are a senior {role}.
Answer clearly and briefly (2–3 sentences).

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,          # IMPORTANT: disable streaming
            "options": {
                "num_predict": 120,   # fast
                "temperature": 0.2
            }
        },
        timeout=60
    )

    data = response.json()
    return data.get("response", "").strip()
