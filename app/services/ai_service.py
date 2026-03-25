"""Service for AI-based ticket priority classification."""
import requests


def get_priority(description):
    """Classify a ticket description into a priority level (P1, P2, or P3)."""
    prompt = f"""
    You are an AI that classifies support tickets.
    Rules:
    - P1: critical issues, system down
    - P2: moderate issues
    - P3: minor issues

    Respond ONLY with: P1, P2, or P3

    Ticket:
    {description}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }, timeout = 30
    )

    result = response.json()
    ai_response = result["response"].strip().upper()

    if ai_response not in ["P1", "P2", "P3"]:
        return "P3"


    return ai_response
