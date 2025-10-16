import React from "react";
import ActiviteCard from "../components/ActiviteCard";
import eveilImg from "../assets/eveil.png";
import laboImg from "../assets/labo.png";
import cursusImg from "../assets/cursus.png";

function Accueil() {
  const activites = [
    { nom: "Éveil", description: "Découverte musicale pour les petits.", image: eveilImg },
    { nom: "Labo", description: "Ateliers pratiques et créatifs.", image: laboImg },
    { nom: "Cursus", description: "Programme complet pour progresser.", image: cursusImg }
  ];

  return (
    <div className="container">
      <h1>Nos activités</h1>
      <div className="activites">
        {activites.map((act, i) => <ActiviteCard key={i} {...act} />)}
      </div>
    </div>
  );
}

export default Accueil;
