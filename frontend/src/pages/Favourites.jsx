import React, { useEffect, useState } from "react";
import RecipeCard from "../components/RecipeCard";

export default function Favourites() {
  const [recipes, setRecipes] = useState([]);

  const loadFavourites = () => {
    fetch("http://127.0.0.1:5000/api/favourites")
      .then((r) => r.json())
      .then((d) => setRecipes(d.recipes || []))
      .catch(() => setRecipes([]));
  };

  useEffect(() => {
    loadFavourites();
  }, []);

  const toggleFav = (name) => {
    fetch("http://127.0.0.1:5000/api/favourite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).then(() => loadFavourites());
  };

  return (
    <div className="space-y-10">

      {/* Header */}
      <div className="p-5 glass-dark ember-glow rounded-xl text-orange-300 text-xl font-semibold text-center">
        Your Favourite Recipes
      </div>

      {/* No favourites */}
      {recipes.length === 0 && (
        <p className="text-center text-gray-400">
          You haven't saved any recipes yet.
        </p>
      )}

      {/* Favourites Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {recipes.map((r, i) => (
          <RecipeCard key={i} r={r} toggleFav={toggleFav} />
        ))}
      </div>
    </div>
  );
}
