import csv
from typing import List, Dict, Tuple, Set


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


def _score_recipe(user_ings: Set[str], recipe: Dict) -> float:
    """Score a recipe based on ingredient overlap (0–1)."""
    recipe_ings = set(recipe.get("ingredients", []))
    if not recipe_ings:
        return 0.0
    matches = user_ings & recipe_ings
    return len(matches) / len(recipe_ings)


def get_suggestions(
    user_input: str, recipes: List[Dict], limit: int = 5
) -> Tuple[List[Dict], str | None]:
    """
    Given a raw ingredient string and a recipe list, return top suggestions
    and an optional error message.
    """
    # Normalise and parse user ingredients
    user_ings = {i.strip().lower() for i in user_input.split(",") if i.strip()}
    if not user_ings:
        return [], "Couldn't read any ingredients. Try separating them with commas."

    scored: List[tuple[Dict, float]] = []
    for recipe in recipes:
        score = _score_recipe(user_ings, recipe)
        if score > 0:
            scored.append((recipe, score))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    suggestions = [r for r, _ in scored[:limit]]

    if not suggestions:
        return [], "No matching recipes found. Try different ingredients or add more."

    return suggestions, None
