import requests


def get_priority(description):
    prompt = f"""
    You are an AI that classifies support tickets.
    Rules:
    - P1: system down; critical business impact; many users affected;
    - P2: partial system issues; degraded performance; some users affected;
    - P3: routine requests; password resets; user creation or updates; non-urgent tasks;

    Respond ONLY with: P1, P2, or P3

    Ticket:
    {description}
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }, timeout=60
        )
        result = response.json()
        ai_response = result.get("response", "").strip().upper()
    except requests.exceptions.RequestException:
        return "P3"

    if ai_response not in ["P1", "P2", "P3"]:
        return "P3"

    return ai_response
