import React, { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import RecipeCard from "../components/RecipeCard";

export default function Home() {
  const [results, setResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const loadHistory = () => {
    fetch("http://127.0.0.1:5000/api/history")
      .then((r) => r.json())
      .then((d) => setHistory(d.history || []))
      .catch(() => {});
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const search = (input) => {
    if (!input.trim()) return;

    setLoading(true);
    setErrorMsg("");

    fetch("http://127.0.0.1:5000/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients: input }),
    })
      .then((r) => r.json())
      .then((d) => {
        setLoading(false);

        if (d.error) {
          setErrorMsg(d.error);
          setResults([]);
        } else {
          setResults(d.recipes || []);
        }

        loadHistory();
      })
      .catch(() => {
        setLoading(false);
        setErrorMsg("ERROR:6767.");
      });
  };

  const toggleFav = (name) => {
    fetch("http://127.0.0.1:5000/api/favourite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).catch(() => {});
  };

  return (
    <div className="space-y-10">

      {/* Search Bar */}
      <SearchBar onSearch={search} />

      {/* Recent Search History */}
      {history.length > 0 && (
        <div className="p-4 glass-dark rounded-xl ember-border">
          <h3 className="text-lg font-semibold text-orange-400 mb-3">
            Recent searches
          </h3>

          <div className="flex flex-wrap gap-2">
            {history.map((item, i) => (
              <button
                key={i}
                onClick={() => search(item)}
                className="
                  px-3 py-1 rounded-lg 
                  bg-black text-orange-300 ember-border 
                  hover:bg-orange-600 hover:text-black 
                  transition
                "
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="text-center text-orange-400 text-lg animate-pulse">
          🔥 Searching...
        </div>
      )}

      {/* Error */}
      {errorMsg && (
        <div className="text-center text-red-400 text-lg">
          {errorMsg}
        </div>
      )}

      {/* Results */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {results.map((r, i) => (
          <RecipeCard key={i} r={r} toggleFav={toggleFav} />
        ))}

        {/* Empty state */}
        {!loading && !errorMsg && results.length === 0 && (
          <p className="text-gray-400 text-center col-span-full">
            Try searching for ingredients above and not down here.
          </p>
        )}
      </div>
    </div>
  );
}
