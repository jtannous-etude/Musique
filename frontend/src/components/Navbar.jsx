import React from "react";
import logo from "../assets/logo.png";

function Navbar() {
  return (
    <nav className="navbar">
      <img src={logo} alt="Logo" />
      <h1>Musique</h1>
    </nav>
  );
}

export default Navbar;
