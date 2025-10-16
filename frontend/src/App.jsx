import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Accueil from "./pages/Accueil";
import Preinscription from "./pages/Preinscription";
import Navbar from "./components/Navbar";
import "./styles/App.css";

function App() {
  return (
    <Router>
      <Navbar />
      <nav>
        <Link to="/">Accueil</Link> | <Link to="/preinscription">Préinscription</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/preinscription" element={<Preinscription />} />
      </Routes>
    </Router>
  );
}

export default App;
