import React, { useEffect, useState, useRef } from "react";

export default function Autosuggest({ query, onPick }) {
  const [data, setData] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const boxRef = useRef(null);

  // ----------------------------------------------------------
  // Fetch suggestions
  // ----------------------------------------------------------
  useEffect(() => {
    if (!query || query.length < 1) {
      setData([]);
      return;
    }

    fetch(`http://127.0.0.1:5000/api/suggest?q=${query}`)
      .then((res) => res.json())
      .then((d) => {
        setData(d.suggestions || []);
        setActiveIndex(0);
      })
      .catch(() => setData([]));
  }, [query]);

  // ----------------------------------------------------------
  // Keyboard navigation
  // ----------------------------------------------------------
  const handleKey = (e) => {
    if (!data.length) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((prev) => (prev + 1) % data.length);
    }

    if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((prev) => (prev - 1 + data.length) % data.length);
    }

    if (e.key === "Enter") {
      e.preventDefault();
      onPick(data[activeIndex]);
    }

    if (e.key === "Escape") {
      setData([]);
    }
  };

  useEffect(() => {
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  });

  // ----------------------------------------------------------
  // Highlight the matching text
  // ----------------------------------------------------------
  const highlight = (item) => {
    const lower = item.toLowerCase();
    const q = query.toLowerCase();
    const idx = lower.indexOf(q);

    if (idx === -1) return item;

    return (
      <>
        {item.slice(0, idx)}
        <span className="text-orange-400 font-bold">
          {item.slice(idx, idx + query.length)}
        </span>
        {item.slice(idx + query.length)}
      </>
    );
  };

  // ----------------------------------------------------------
  // Render "no suggestions" box
  // ----------------------------------------------------------
  if (!data.length) {
    return (
      <div
        className="
          absolute w-full mt-2 p-2 rounded-xl 
          ember-border no-blur
          text-gray-400 text-sm
          animate-fadeIn animate-slideUp
          z-[9999]
        "
      >
        <div className="px-3 py-2">No suggestions</div>
      </div>
    );
  }

  // ----------------------------------------------------------
  // Render suggestions list
  // ----------------------------------------------------------
  return (
    <div
      ref={boxRef}
      className="
        absolute w-full mt-2 max-h-60 overflow-y-auto
        rounded-xl p-2 ember-border no-blur
        animate-fadeIn animate-slideUp
        z-[9999]
      "
    >
      {data.map((item, idx) => (
        <div
          key={idx}
          className={`
            px-3 py-2 rounded-lg cursor-pointer transition
            ${
              idx === activeIndex
                ? "bg-orange-600 text-black"
                : "hover:bg-orange-600 hover:text-black"
            }
          `}
          onClick={() => onPick(item)}
        >
          {highlight(item)}
        </div>
      ))}
    </div>
  );
}
