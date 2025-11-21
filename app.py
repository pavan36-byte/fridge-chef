from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

def load_recipes():
    recipes = []
    csv_path = os.path.join(os.path.dirname(__file__), "recipes.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # store ingredients as a list
            row["ingredients"] = [i.strip().lower() for i in row["ingredients"].split(",")]
            recipes.append(row)
    return recipes

RECIPES = load_recipes()

def score_recipe(user_ings, recipe):
    recipe_ings = set(recipe["ingredients"])
    if not recipe_ings:
        return 0
    # how many user ingredients appear in this recipe
    matches = recipe_ings & user_ings
    # simple score: fraction of recipe ingredients you have
    score = len(matches) / len(recipe_ings)
    return score

@app.route("/", methods=["GET", "POST"])
def index():
    suggestions = []
    user_input = ""
    error = None

    if request.method == "POST":
        user_input = request.form.get("ingredients", "").strip().lower()

        if not user_input:
            error = "Please enter at least one ingredient."
        else:
            # parse user ingredients
            user_ings = {i.strip() for i in user_input.split(",") if i.strip()}
            if not user_ings:
                error = "Couldn't read any ingredients. Try separating them with commas."
            else:
                scored = []
                for recipe in RECIPES:
                    score = score_recipe(user_ings, recipe)
                    if score > 0:
                        scored.append((recipe, score))

                scored.sort(key=lambda x: x[1], reverse=True)
                suggestions = [r for r, s in scored[:5]]

                if not suggestions:
                    error = "No matching recipes found. Try different ingredients."

    return render_template(
        "index.html",
        suggestions=suggestions,
        user_input=user_input,
        error=error,
    )

if __name__ == "__main__":
    app.run(debug=True)
