import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Home from "./pages/Home";
import Favourites from "./pages/Favourites";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen p-4 text-white relative z-20">

        {/* Header */}
        <header className="text-center py-6">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
            || Fridge Chef ||
          </h1>
          <p className="text-gray-400 mt-2">
            Find meals using the ingredients you already have - Made by Pavan Gill
          </p>
        </header>

        {/* Nav */}
        <nav className="flex justify-center gap-6 mt-4">
          <Link className="ember-glow px-4 py-2 rounded-lg" to="/">Home</Link>
          <Link className="ember-glow px-4 py-2 rounded-lg" to="/favourites">Favourites</Link>
        </nav>

        {/* Main content */}
        <main className="mt-10 max-w-4xl mx-auto relative z-30">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/favourites" element={<Favourites />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
