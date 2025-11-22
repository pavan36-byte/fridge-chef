import csv

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

def load_recipes(csv_path: str):
    recipes = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            if not name or name.lower() == "name":
                continue

            raw_ings = row.get("ingredients", "")
            ingredients = [normalise(i) for i in raw_ings.split(",") if i.strip()]

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

def match_recipes(user_ingredients, recipes):
    user_set = {normalise(i) for i in user_ingredients}
    results = []

    for r in recipes:
        ings = r["ingredients"]
        ing_set = set(ings)
        matched_set = ing_set & user_set

        matched = len(matched_set)
        total = len(ings)
        missing = list(ing_set - user_set)

        score = matched / total if total else 0
        match_percent = int(score * 100)

        if match_percent >= 80:
            cookability = "can_cook"
        elif match_percent >= 50:
            cookability = "almost"
        else:
            cookability = "unlikely"

        results.append({
            "name": r["name"],
            "description": r["description"],
            "ingredients": ings,
            "cuisine": r["cuisine"],
            "type": r["type"],
            "difficulty": r["difficulty"],
            "time_minutes": r["time_minutes"],
            "matched": matched,
            "total": total,
            "missing": missing,
            "match_percent": match_percent,
            "cookability": cookability
        })

    results.sort(key=lambda x: x["match_percent"], reverse=True)
    return results
