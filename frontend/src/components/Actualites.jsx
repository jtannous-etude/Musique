import React from "react";
import { useNavigate } from "react-router-dom";

function Actualites() {
  const navigate = useNavigate();

  return (
    <div className="container" style={{ marginTop: "40px", textAlign: "center", border: "1px solid orange", borderRadius: "10px", padding: "20px", backgroundColor: "#fff7f0" }}>
      <h2>Ouverture des préinscriptions</h2>
      <p>Inscrivez votre enfant dès maintenant pour nos activités musicales !</p>
      <button onClick={() => navigate("/preinscription")}>Préinscription</button>
    </div>
  );
}

export default Actualites;
