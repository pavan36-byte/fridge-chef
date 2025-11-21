from flask import Flask, render_template, request
from utils import (
    load_recipes,
    load_state,
    save_state,
    get_suggestions,
)

app = Flask(__name__)

RECIPES = load_recipes("recipes.csv")
STATE_PATH = "state.json"


@app.route("/", methods=["GET", "POST"])
def index():
    # Load persistent state (search history + favourites)
    state = load_state(STATE_PATH)
    search_history = state.get("search_history", [])
    favourites = state.get("favourites", [])

    suggestions = []
    error: str | None = None
    user_input = ""
    sort_by = "best"

    if request.method == "POST":
        action = request.form.get("action", "search")
        user_input = request.form.get("ingredients", "").strip()
        sort_by = request.form.get("sort_by", "best") or "best"

        # --- HANDLE FAVOURITES TOGGLE ---
        if action == "favorite":
            recipe_name = request.form.get("recipe_name", "").strip()
            if recipe_name:
                if recipe_name in favourites:
                    favourites.remove(recipe_name)
                else:
                    favourites.append(recipe_name)
                state["favourites"] = favourites
                save_state(STATE_PATH, state)

            # After updating favourites, re-run suggestions for the same search (if any)
            if user_input:
                suggestions, error = get_suggestions(
                    user_input, RECIPES, sort_by, favourites, limit=8
                )

        # --- HANDLE NORMAL SEARCH ---
        else:
            if not user_input:
                error = "Please enter at least one ingredient."
            elif len(user_input) > 200:
                error = "That’s a lot of text! Try listing only ingredients, separated by commas."
            else:
                suggestions, error = get_suggestions(
                    user_input, RECIPES, sort_by, favourites, limit=8
                )

                # Update search history only if search was valid
                if not error and user_input:
                    # Remove if already exists, then insert at front (no duplicates)
                    if user_input in search_history:
                        search_history.remove(user_input)
                    search_history.insert(0, user_input)
                    # Keep only last 5 searches
                    search_history = search_history[:5]
                    state["search_history"] = search_history
                    save_state(STATE_PATH, state)

    return render_template(
        "index.html",
        suggestions=suggestions,
        user_input=user_input,
        error=error,
        search_history=search_history,
        sort_by=sort_by,
        favourites=favourites,
    )


if __name__ == "__main__":
    app.run(debug=True)
