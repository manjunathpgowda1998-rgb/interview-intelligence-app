import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"   # fastest on CPU

def generate_answer(question: str, role: str) -> str:
    """
    Generates a fast, concise interview-style answer.
    """
    prompt = f"""
Role: {role}
Answer in 3 short bullet points.
Be direct and technical.
No explanations.

Q: {question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 80,
                "temperature": 0.2,
                "top_p": 0.9
            }
        },
        timeout=20
    )

    return response.json().get("response", "").strip()
