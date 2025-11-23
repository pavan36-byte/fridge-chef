import React, { useState, useEffect, useRef } from "react";
import Autosuggest from "./Autosuggest";

export default function SearchBar({ onSearch }) {
  const [input, setInput] = useState("");
  const [showSuggest, setShowSuggest] = useState(false);

  const wrapperRef = useRef(null);

  // ----------------------------------------------------------
  // Close autosuggest when clicking outside
  // ----------------------------------------------------------
  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowSuggest(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // ----------------------------------------------------------
  // Submit search
  // ----------------------------------------------------------
  const submit = (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    onSearch(input);
    setShowSuggest(false);
  };

  return (
    <div
      ref={wrapperRef}
      className="relative w-full z-[10000]"  
      /* This z-index gives autosuggest room but doesn't interfere with cards/modal */
    >
      {/* Input */}
      <form onSubmit={submit}>
        <input
          className="w-full p-4 glass-dark ember-border rounded-xl focus:outline-none"
          placeholder="I've got chicken, rice, tomatoes..."
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            setShowSuggest(true);
          }}
          onKeyDown={(e) => {
            if (e.key === "Escape") {
              setShowSuggest(false);
            }
          }}
        />
      </form>

      {/* Autosuggest dropdown */}
      {showSuggest && input.length >= 1 && (
        <div className="absolute top-full left-0 w-full mt-2 z-[10000]">
          <Autosuggest
            query={input}
            onPick={(value) => {
              setInput(value);
              onSearch(value);
              setShowSuggest(false);
            }}
          />
        </div>
      )}
    </div>
  );
}
