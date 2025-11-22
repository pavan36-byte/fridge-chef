import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def ai_single_call(user_text: str, recipe_names: list[str]) -> dict:
    prompt = {
        "role": "user",
        "content": (
            "Extract ingredients from this text. "
            "Return JSON ONLY with keys 'ingredients' and 'explanations'. "
            "ingredients must be a list of simple food words only. "
            "explanations must be a dictionary where keys are recipe names. "
            "Do NOT add extra commentary.\n\n"
            f"User input: {user_text}\n\n"
            f"Recipes: {recipe_names}"
        )
    }

    payload = {
        "model": MODEL,
        "prompt": json.dumps(prompt),
        "stream": False
        }

    response = requests.post(OLLAMA_URL, json=payload)
    raw = response.json().get("response", "").strip()

    print("\n======= RAW AI OUTPUT =======")
    print(raw)
    print("======= END =======\n")

    cleaned = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except:
        pass

    return {"ingredients": [], "explanations": {}}
