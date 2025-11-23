from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import load_recipes, match_recipes, load_state, save_state, normalise
from ai_utils import ai_single_call

app = Flask(__name__)
CORS(app)

RECIPES = load_recipes("recipes.csv")
STATE = load_state()


# ----------------------------------------------------------
#  SEARCH (AI-powered)
# ----------------------------------------------------------

@app.post("/api/search")
def api_search():
    data = request.json
    text = (data.get("ingredients") or "").strip()

    # Save search history
    if text and text not in STATE["history"]:
        STATE["history"].insert(0, text)
        STATE["history"] = STATE["history"][:8]
        save_state(STATE)

    # Base ranking to give AI context of top recipes
    base = match_recipes([], RECIPES)
    top_recipe_names = [r["name"] for r in base[:8]]

    # AI ingredient extraction + reasoning
    ai = ai_single_call(text, top_recipe_names)
    extracted = ai.get("ingredients", [])
    explanations = ai.get("explanations", {})

    # If AI failed to extract anything, return empty
    if not extracted:
        return jsonify({"recipes": [], "error": "No ingredients detected."})

    # Run scoring
    results = match_recipes(extracted, RECIPES)

    # Enrich results for front-end
    enriched = []
    for r in results[:12]:
        enriched.append({
            "name": r["name"],
            "description": r["description"],
            "ingredients": r["ingredients"],
            "cuisine": r["cuisine"],
            "type": r["type"],
            "difficulty": r["difficulty"],
            "time_minutes": r["time_minutes"],
            "matched": r["matched"],
            "total": r["total"],
            "missing": r["missing"],
            "match_percent": r["match_percent"],
            "cookability": r["cookability"],
            "is_favourite": r["name"] in STATE["favourites"],
            "explanation": explanations.get(r["name"], "")
        })

    return jsonify({"recipes": enriched})


# ----------------------------------------------------------
#  SAVE / UNSAVE FAVOURITE
# ----------------------------------------------------------

@app.post("/api/favourite")
def api_fav():
    name = request.json.get("name")

    if not name:
        return jsonify({"error": "No recipe name supplied."})

    if name in STATE["favourites"]:
        STATE["favourites"].remove(name)
    else:
        STATE["favourites"].append(name)

    save_state(STATE)
    return jsonify({"ok": True})


# ----------------------------------------------------------
#  GET FAVOURITES (FULL RECIPE DATA)
# ----------------------------------------------------------

@app.get("/api/favourites")
def api_get_favs():
    fav_list = []
    for r in RECIPES:
        if r["name"] in STATE["favourites"]:
            fav_list.append({
                **r,
                "matched": 0,
                "total": len(r["ingredients"]),
                "missing": r["ingredients"],
                "match_percent": 0,
                "cookability": "unknown",
                "is_favourite": True,
                "explanation": ""
            })
    return jsonify({"recipes": fav_list})


# ----------------------------------------------------------
#  AUTO-SUGGEST (ingredient autocomplete)
# ----------------------------------------------------------

@app.get("/api/suggest")
def api_suggest():
    q = request.args.get("q", "").strip().lower()

    if len(q) < 1:
        return jsonify({"suggestions": []})

    # Collect all ingredients from dataset
    all_ings = set(i for r in RECIPES for i in r["ingredients"])

    # Filter by substring match
    suggestions = [i for i in all_ings if q in i][:8]

    return jsonify({"suggestions": suggestions})


# ----------------------------------------------------------
#  SEARCH HISTORY
# ----------------------------------------------------------

@app.get("/api/history")
def api_history():
    return jsonify({"history": STATE["history"]})


# ----------------------------------------------------------
#  EXPLANATION ON DEMAND
# ----------------------------------------------------------

@app.get("/api/explain")
def api_explain():
    name = request.args.get("name")
    if not name:
        return jsonify({"explanation": ""})

    # Ask AI for ONLY this recipe's reasoning
    ai = ai_single_call(f"Explain why {name} fits the provided ingredients.", [name])
    explanation = ai.get("explanations", {}).get(name, "")

    return jsonify({"explanation": explanation})


# ----------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
