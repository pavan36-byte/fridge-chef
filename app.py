from flask import Flask, render_template, request
from utils import load_recipes, get_suggestions

app = Flask(__name__)

# Load recipes once when the app starts
RECIPES = load_recipes("recipes.csv")


@app.route("/", methods=["GET", "POST"])
def index():
    suggestions = []
    error = None
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("ingredients", "").strip()

        # Basic input validation
        if not user_input:
            error = "Please enter at least one ingredient."
        elif len(user_input) > 200:
            error = "That’s a lot of text! Try listing only ingredients, separated by commas."
        else:
            suggestions, error = get_suggestions(user_input, RECIPES, limit=8)

    return render_template(
        "index.html",
        suggestions=suggestions,
        user_input=user_input,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
