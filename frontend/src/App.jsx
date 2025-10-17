import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Accueil from "./pages/Accueil";
import Preinscription from "./pages/Preinscription";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./styles/App.css";

function App() {
  return (
    <Router>
      <Navbar />

      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/preinscription" element={<Preinscription />} />
      </Routes>

      <Footer /> 
    </Router>
  );
}


export default App;
