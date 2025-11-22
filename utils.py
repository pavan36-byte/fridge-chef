import csv
import json
import os
from typing import List, Dict, Tuple, Set

# ---------- INGREDIENT NORMALISATION ----------

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
}

def normalise(ingredient: str) -> str:
    ingredient = ingredient.strip().lower()
    return NORMALISE_MAP.get(ingredient, ingredient)


# ---------- DATA LOADING ----------

def load_recipes(csv_path: str) -> List[Dict]:
    recipes: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_ings = row.get("ingredients", "")
            clean_ings = [normalise(i) for i in raw_ings.split(",") if i.strip()]

            recipes.append({
                "name": row.get("name", "").strip(),
                "description": row.get("description", "").strip(),
                "ingredients": clean_ings,
                "cuisine": row.get("cuisine", "Unknown"),
                "type": row.get("type", "Main"),
                "difficulty": row.get("difficulty", "Easy"),
                "time_minutes": int(row.get("time_minutes", 20)),
            })
    return recipes


# ---------- STATE (HISTORY + FAVOURITES) ----------

def load_state(path: str) -> Dict:
    if not os.path.exists(path):
        return {"search_history": [], "favourites": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("search_history", [])
            data.setdefault("favourites", [])
            return data
    except Exception:
        return {"search_history": [], "favourites": []}

def save_state(path: str, state: Dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ---------- SCORING + SUGGESTIONS ----------

def _score_recipe(user_ings: Set[str], recipe: Dict):
    recipe_ings = set(recipe["ingredients"])
    total = len(recipe_ings)

    matches = user_ings & recipe_ings
    matched = len(matches)
    missing = list(recipe_ings - user_ings)
    missing_count = len(missing)

    score = matched / total if total else 0
    match_percent = int(score * 100)

    # Cookability classification
    if match_percent >= 80:
        cookability = "can_cook"
    elif match_percent >= 50:
        cookability = "almost"
    else:
        cookability = "unlikely"

    return {
        "score": score,
        "match_percent": match_percent,
        "matched": matched,
        "total": total,
        "missing": missing,
        "cookability": cookability,
    }


def get_suggestions(
    user_input: str,
    recipes: List[Dict],
    sort_by: str,
    favourites: List[str],
    limit: int = 10,
):

    user_ings = {normalise(i.strip()) for i in user_input.split(",") if i.strip()}
    if not user_ings:
        return [], "Couldn't read any ingredients. Try commas."

    enriched = []

    for recipe in recipes:
        scoring = _score_recipe(user_ings, recipe)

        if scoring["score"] > 0:
            enriched.append({
                **recipe,
                **scoring,
                "is_favourite": recipe["name"] in favourites,
            })

    if not enriched:
        return [], "No matching recipes found."

    # Sorting logic
    if sort_by == "least_missing":
        enriched.sort(key=lambda x: (len(x["missing"]), -x["score"]))
    elif sort_by == "simplest":
        enriched.sort(key=lambda x: (x["total"], -x["score"]))
    else:
        enriched.sort(key=lambda x: (-x["score"], x["total"]))

    return enriched[:limit], None
