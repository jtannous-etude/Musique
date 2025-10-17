import React from "react";
import { Link } from "react-router-dom";
import "../styles/App.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <p>&copy; {new Date().getFullYear()} MonSite. Tous droits réservés.</p>
        
      </div>
    </footer>
  );
}

export default Footer;