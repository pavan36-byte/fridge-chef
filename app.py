from flask import Flask, render_template, request
from utils import load_recipes, match_recipes, load_state, save_state, get_suggestions
from ai_utils import ai_single_call

app = Flask(__name__)

RECIPES = load_recipes("recipes.csv")
STATE = load_state()


@app.route("/", methods=["GET", "POST"])
def index():
    suggestions = []
    error = None
    user_input = ""
    sort_by = request.form.get("sort_by", "best_match")

    if request.method == "POST":
        user_input = (request.form.get("ingredients") or "").strip()

        if not user_input:
            return render_template(
                "index.html",
                suggestions=[],
                history=STATE["history"],
                favourites=STATE["favourites"],
                user_input="",
                error="Enter some ingredients.",
            )

        if user_input not in STATE["history"]:
            STATE["history"].insert(0, user_input)
            STATE["history"] = STATE["history"][:8]
            save_state(STATE)

        base = match_recipes([], RECIPES)
        top_names = [r["name"] for r in base[:8]]

        ai = ai_single_call(user_input, top_names)
        extracted = ai.get("ingredients", [])
        explanations = ai.get("explanations", {})

        if not extracted:
            return render_template(
                "index.html",
                suggestions=[],
                history=STATE["history"],
                favourites=STATE["favourites"],
                user_input=user_input,
                error="I couldn't read any ingredients.",
            )

        suggestions = match_recipes(extracted, RECIPES)
        suggestions = suggestions[:8]

        for r in suggestions:
            r["explanation"] = explanations.get(r["name"], "")
            r["is_favourite"] = r["name"] in STATE["favourites"]

    return render_template(
        "index.html",
        suggestions=suggestions,
        history=STATE["history"],
        favourites=STATE["favourites"],
        user_input=user_input,
        error=error,
    )


@app.route("/fav", methods=["POST"])
def fav():
    name = request.form.get("recipe_name")

    if name:
        if name in STATE["favourites"]:
            STATE["favourites"].remove(name)
        else:
            STATE["favourites"].append(name)

        save_state(STATE)

    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)
