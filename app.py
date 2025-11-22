from flask import Flask, render_template, request
from utils import load_recipes, match_recipes
from ai_utils import ai_single_call

app = Flask(__name__)
RECIPES = load_recipes("recipes.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    suggestions = []
    error = None
    user_input = ""

    if request.method == "POST":
        user_input = (request.form.get("ingredients") or "").strip()

        if not user_input:
            error = "Enter some ingredients."
            return render_template("index.html", suggestions=[], user_input="", error=error)

        base = match_recipes([], RECIPES)
        names = [r["name"] for r in base[:8]]

        ai = ai_single_call(user_input, names)
        extracted = ai.get("ingredients", [])
        explanations = ai.get("explanations", {})

        if not extracted:
            error = "I couldn't read any ingredients."
            return render_template("index.html", suggestions=[], user_input=user_input, error=error)

        matches = match_recipes(extracted, RECIPES)
        suggestions = matches[:8]

        for r in suggestions:
            r["explanation"] = explanations.get(r["name"], "")

    return render_template("index.html", suggestions=suggestions, user_input=user_input, error=error)

if __name__ == "__main__":
    app.run(debug=True)
