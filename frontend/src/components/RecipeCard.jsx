import React, { useState } from "react";
import Modal from "./Modal";

export default function RecipeCard({ r, toggleFav }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [explanation, setExplanation] = useState("");

  // ----------------------------------------------------------
  // Load AI explanation when opening modal
  // ----------------------------------------------------------
  const loadExplanation = () => {
    setLoading(true);

    fetch(`http://127.0.0.1:5000/api/explain?name=${encodeURIComponent(r.name)}`)
      .then((res) => res.json())
      .then((data) => {
        setExplanation(data.explanation || "No explanation available.");
        setLoading(false);
      })
      .catch(() => {
        setExplanation("Could not load explanation.");
        setLoading(false);
      });
  };

  const openModal = () => {
    setOpen(true);
    loadExplanation();
  };

  // ----------------------------------------------------------
  // Cookability visuals
  // ----------------------------------------------------------
  const cookabilityText = {
    can_cook: "You can cook this!",
    almost: `Almost — missing ${r.missing?.length || 0} ingredient${
      (r.missing?.length || 0) !== 1 ? "s" : ""
    }`,
    unlikely: "Missing too many ingredients",
    unknown: "Cookability unknown",
  };

  const cookabilityColor = {
    can_cook: "text-green-400",
    almost: "text-yellow-300",
    unlikely: "text-red-400",
    unknown: "text-gray-400",
  };

  return (
    <div className="glass-dark ember-glow p-5 rounded-xl space-y-3 relative">

      {/* Header */}
      <div className="flex justify-between items-center">
        <h3 className="text-xl font-bold text-orange-300">{r.name}</h3>

        <button
          className={`
            px-3 py-1 rounded-lg transition
            ${
              r.is_favourite
                ? "bg-orange-600 text-black"
                : "bg-black text-orange-400 ember-border hover:bg-orange-600 hover:text-black"
            }
          `}
          onClick={() => toggleFav(r.name)}
        >
          {r.is_favourite ? "★" : "☆"}
        </button>
      </div>

      {/* Match Summary */}
      <div className="text-sm text-gray-300">
        <span className="font-semibold text-orange-400">
          {r.match_percent}% match
        </span>
        {" — "}
        {r.matched}/{r.total} ingredients
      </div>

      {/* Cookability */}
      <div className={`${cookabilityColor[r.cookability]} font-semibold`}>
        {cookabilityText[r.cookability]}
      </div>

      {/* Missing ingredients */}
      {r.missing && r.missing.length > 0 && (
        <div className="text-red-300 text-sm">
          <strong>Missing:</strong> {r.missing.join(", ")}
        </div>
      )}

      {/* Tags */}
      <div className="text-sm flex flex-wrap gap-2 text-gray-300">
        <span className="px-2 py-1 rounded bg-black ember-border">
          🌍 {r.cuisine}
        </span>
        <span className="px-2 py-1 rounded bg-black ember-border">
          🍽 {r.type}
        </span>
        <span className="px-2 py-1 rounded bg-black ember-border">
          ⚙ {r.difficulty}
        </span>
        <span className="px-2 py-1 rounded bg-black ember-border">
          ⏱ {r.time_minutes} min
        </span>
      </div>

      {/* Description */}
      {r.description && (
        <p className="text-gray-300 text-sm">{r.description}</p>
      )}

      {/* Ingredients */}
      <p className="text-gray-400 text-sm">
        <strong className="text-orange-400">Ingredients:</strong>{" "}
        {r.ingredients?.join(", ")}
      </p>

      {/* Why button */}
      <button
        className="
          mt-2 px-4 py-2 
          bg-gradient-to-r from-orange-600 to-red-600 
          rounded-lg text-black font-semibold 
          hover:opacity-90 transition
        "
        onClick={openModal}
      >
        Why this recipe?
      </button>

      {/* Modal */}
      {open && (
        <Modal onClose={() => setOpen(false)}>
          <h2 className="text-xl font-bold mb-3 text-orange-300">{r.name}</h2>

          {loading ? (
            <p className="text-orange-400 animate-pulse">
              Loading explanation...
            </p>
          ) : (
            <p className="text-gray-200 whitespace-pre-line">{explanation}</p>
          )}
        </Modal>
      )}
    </div>
  );
}
