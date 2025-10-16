import React from "react";

function ActiviteCard({ nom, description, image }) {
  return (
    <div className="activite-card">
      <img src={image} alt={nom} />
      <h3>{nom}</h3>
      <p>{description}</p>
    </div>
  );
}

export default ActiviteCard;
