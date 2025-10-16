import React from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";
import "../styles/App.css";

function Navbar() {
  return (
    <nav className="navbar">
      <img src={logo} alt="Logo" />
      <h1>Musique</h1>
      <div className="navbar-links">
        <Link to="/">Accueil</Link>
        <Link to="/preinscription">Préinscription</Link>
      </div>
    </nav>
  );
}

export default Navbar;
