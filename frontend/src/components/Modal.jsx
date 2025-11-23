import React, { useEffect, useRef } from "react";

export default function Modal({ children, onClose }) {
  const boxRef = useRef(null);

  // ----------------------------------------------------------
  // Close when clicking outside
  // ----------------------------------------------------------
  useEffect(() => {
    function handleClick(e) {
      if (boxRef.current && !boxRef.current.contains(e.target)) {
        onClose();
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [onClose]);

  // ----------------------------------------------------------
  // Close with Escape key
  // ----------------------------------------------------------
  useEffect(() => {
    function handleEsc(e) {
      if (e.key === "Escape") onClose();
    }
    document.addEventListener("keydown", handleEsc);
    return () => document.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  return (
    <div
      className="
        fixed inset-0 
        bg-black/75 backdrop-blur-sm
        flex items-center justify-center
        z-[20000]
        animate-fadeIn
      "
    >
      <div
        ref={boxRef}
        className="
          w-[90%] max-w-md
          glass-dark ember-glow 
          rounded-xl p-6
          animate-scaleIn
        "
      >
        {children}

        <button
          className="
            mt-6 w-full 
            py-2 rounded-lg 
            bg-gradient-to-r from-red-600 to-orange-600 
            text-black font-semibold 
            hover:opacity-85 
            transition
          "
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </div>
  );
}
