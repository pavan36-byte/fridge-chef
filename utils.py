import csv
import json
import os
from typing import List, Dict, Tuple, Set


# ---------- DATA LOADING ----------


def load_recipes(csv_path: str) -> List[Dict]:
    """Load recipes from a CSV file."""
    recipes: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["ingredients"] = _parse_ingredient_list(row.get("ingredients", ""))
            row["name"] = row.get("name", "").strip()
            row["description"] = row.get("description", "").strip()
            recipes.append(row)
    return recipes


def _parse_ingredient_list(ings: str) -> List[str]:
    """Convert a comma-separated ingredient string into a clean list."""
    return [i.strip().lower() for i in ings.split(",") if i.strip()]


# ---------- STATE (HISTORY + FAVOURITES) ----------


def load_state(path: str) -> Dict:
    """Load search history and favourites from JSON. Returns default if missing or invalid."""
    if not os.path.exists(path):
        return {"search_history": [], "favourites": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure keys exist
            if "search_history" not in data:
                data["search_history"] = []
            if "favourites" not in data:
                data["favourites"] = []
            return data
    except Exception:
        # If file is corrupted or unreadable, start fresh
        return {"search_history": [], "favourites": []}


def save_state(path: str, state: Dict) -> None:
    """Save search history and favourites to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ---------- RECOMMENDATION LOGIC ----------


def _score_recipe(user_ings: Set[str], recipe: Dict) -> Tuple[float, int, int]:
    """
    Score a recipe based on ingredient overlap.

    Returns:
        score (0-1 float),
        matched_count (int),
        total_ingredients (int)
    """
    recipe_ings = set(recipe.get("ingredients", []))
    total = len(recipe_ings)
    if total == 0:
        return 0.0, 0, 0

    matches = user_ings & recipe_ings
    matched_count = len(matches)
    score = matched_count / total
    return score, matched_count, total


def get_suggestions(
    user_input: str,
    recipes: List[Dict],
    sort_by: str,
    favourites: List[str],
    limit: int = 5,
) -> Tuple[List[Dict], str | None]:
    """
    Given a raw ingredient string and recipe list, return enriched suggestions
    and an optional error message.
    """
    # Parse user ingredients
    user_ings: Set[str] = {i.strip().lower() for i in user_input.split(",") if i.strip()}
    if not user_ings:
        return [], "Couldn't read any ingredients. Try separating them with commas."

    enriched: List[Dict] = []
    for recipe in recipes:
        score, matched_count, total_ings = _score_recipe(user_ings, recipe)
        if score <= 0:
            continue

        missing = max(total_ings - matched_count, 0)
        match_percent = int(round(score * 100))

        enriched.append(
            {
                "name": recipe.get("name", ""),
                "description": recipe.get("description", ""),
                "ingredients": recipe.get("ingredients", []),
                "score": score,
                "match_percent": match_percent,
                "matched": matched_count,
                "total": total_ings,
                "missing": missing,
                "is_favourite": recipe.get("name", "") in favourites,
            }
        )

    if not enriched:
        return [], "No matching recipes found. Try different ingredients or add more."

    # Sorting logic
    sort_by = (sort_by or "best").lower()
    if sort_by == "least_missing":
        enriched.sort(key=lambda r: (r["missing"], -r["score"], r["total"]))
    elif sort_by == "simplest":
        enriched.sort(key=lambda r: (r["total"], -r["score"], r["missing"]))
    else:  # "best"
        enriched.sort(key=lambda r: (-r["score"], r["missing"], r["total"]))

    return enriched[:limit], None
