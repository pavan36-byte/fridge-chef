import csv
import json
import os
from typing import List, Dict, Set


# ------------------- NORMALISATION -------------------

NORMALISE_MAP = {
    "tomatoes": "tomato",
    "diced tomatoes": "tomato",
    "fresh tomato": "tomato",
    "eggs": "egg",
    "egg yolk": "egg",
    "egg whites": "egg",
    "noodles": "noodle",
    "spaghetti pasta": "pasta",
    "hot chili": "chili",
    "chilies": "chili",
    "bell peppers": "bell pepper",
    "capsicum": "bell pepper",
    "cheez": "cheese",
    "chicken breast": "chicken",
}

def normalise(ingredient: str) -> str:
    ingredient = ingredient.strip().lower()
    return NORMALISE_MAP.get(ingredient, ingredient)



# ------------------- DATA LOADING -------------------

def load_recipes(csv_path: str) -> List[Dict]:
    recipes = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = (row.get("name") or "").strip()
            if not name or name.lower() == "name":
                continue

            raw = row.get("ingredients", "")
            ingredients = [normalise(i) for i in raw.split(",") if i.strip()]

            raw_time = (row.get("time_minutes") or "").strip()
            try:
                time_minutes = int(raw_time)
            except:
                time_minutes = 20

            recipes.append({
                "name": name,
                "description": (row.get("description") or "").strip(),
                "ingredients": ingredients,
                "cuisine": row.get("cuisine", "Unknown"),
                "type": row.get("type", "Main"),
                "difficulty": row.get("difficulty", "Easy"),
                "time_minutes": time_minutes,
            })

    return recipes



# ------------------- MATCHING -------------------

def score_recipe(user_set: Set[str], r: Dict):
    ing_set = set(r["ingredients"])
    matched_set = user_set & ing_set

    matched = len(matched_set)
    total = len(ing_set)
    missing = list(ing_set - user_set)

    score = matched / total if total else 0
    percent = int(score * 100)

    if percent >= 80:
        cookability = "can_cook"
    elif percent >= 50:
        cookability = "almost"
    else:
        cookability = "unlikely"

    return {
        "matched": matched,
        "total": total,
        "missing": missing,
        "match_percent": percent,
        "cookability": cookability,
        "score": score,
    }


def match_recipes(user_ingredients: List[str], recipes: List[Dict]) -> List[Dict]:
    user_set = {normalise(i) for i in user_ingredients if i}
    results = []

    for r in recipes:
        scoring = score_recipe(user_set, r)

        results.append({
            **r,
            **scoring
        })

    results.sort(key=lambda x: x["match_percent"], reverse=True)
    return results



# ------------------- STATE MANAGEMENT -------------------

STATE_FILE = "state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"history": [], "favourites": []}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("history", [])
            data.setdefault("favourites", [])
            return data
    except:
        return {"history": [], "favourites": []}


def save_state(state: Dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)



# ------------------- HIGH-LEVEL SUGGESTION SYSTEM -------------------

def get_suggestions(
    user_input: str,
    recipes: List[Dict],
    sort_by: str,
    favourites: List[str],
):

    user_set = {normalise(i.strip()) for i in user_input.split(",") if i.strip()}

    if not user_set:
        return [], "I couldn't read any ingredients."

    enriched = []

    for r in recipes:
        scoring = score_recipe(user_set, r)
        if scoring["score"] > 0:
            enriched.append({
                **r,
                **scoring,
                "is_favourite": r["name"] in favourites,
            })

    if not enriched:
        return [], "No matching recipes found."

    if sort_by == "least_missing":
        enriched.sort(key=lambda x: (len(x["missing"]), -x["score"]))
    elif sort_by == "simplest":
        enriched.sort(key=lambda x: (x["total"], -x["score"]))
    else:
        enriched.sort(key=lambda x: (-x["score"], x["total"]))

    return enriched[:12], None
