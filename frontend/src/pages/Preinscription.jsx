import React, { useState } from "react";

function Preinscription() {
  const [formData, setFormData] = useState({
    nom_eleve: "",
    prenom_eleve: "",
    date_naissance: "",
    activite: "eveil",
    nom_representant: "",
    prenom_representant: "",
    telephone: "",
    adresse: ""
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/preinscriptions/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        alert("Préinscription réussie !");
        setFormData({
          nom_eleve: "",
          prenom_eleve: "",
          date_naissance: "",
          activite: "eveil",
          nom_representant: "",
          prenom_representant: "",
          telephone: "",
          adresse: ""
        });
      } else {
        alert("Erreur lors de l'envoi.");
      }
    } catch (err) {
      console.error(err);
      alert("Erreur réseau.");
    }
  };

  return (
    <div>
      <h1>Préinscription</h1>
      <form onSubmit={handleSubmit}>
        <h2>Élève</h2>
        <input type="text" name="nom_eleve" value={formData.nom_eleve} onChange={handleChange} placeholder="Nom" required />
        <input type="text" name="prenom_eleve" value={formData.prenom_eleve} onChange={handleChange} placeholder="Prénom" required />
        <input type="date" name="date_naissance" value={formData.date_naissance} onChange={handleChange} required />
        <select name="activite" value={formData.activite} onChange={handleChange}>
          <option value="eveil">Éveil</option>
          <option value="labo">Labo</option>
          <option value="cursus">Cursus</option>
        </select>

        <h2>Représentant</h2>
        <input type="text" name="nom_representant" value={formData.nom_representant} onChange={handleChange} placeholder="Nom" required />
        <input type="text" name="prenom_representant" value={formData.prenom_representant} onChange={handleChange} placeholder="Prénom" required />
        <input type="tel" name="telephone" value={formData.telephone} onChange={handleChange} placeholder="Téléphone" required />
        <input type="text" name="adresse" value={formData.adresse} onChange={handleChange} placeholder="Adresse" required />

        <button type="submit">Envoyer</button>
      </form>
    </div>
  );
}

export default Preinscription;
