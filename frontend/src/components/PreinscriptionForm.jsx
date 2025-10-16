import React, { useState } from "react";

function PreinscriptionForm() {
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

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/eleves/", {
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
    <form onSubmit={handleSubmit} className="container">
      <h2>Élève</h2>
      {["nom_eleve","prenom_eleve","date_naissance"].map((field, i) => (
        <div className="form-group" key={i}>
          <input
            type={field==="date_naissance"?"date":"text"}
            name={field}
            placeholder={field.replace("_"," ").toUpperCase()}
            value={formData[field]}
            onChange={handleChange}
            required
          />
        </div>
      ))}
      <div className="form-group">
        <select name="activite" value={formData.activite} onChange={handleChange}>
          <option value="eveil">Éveil</option>
          <option value="labo">Labo</option>
          <option value="cursus">Cursus</option>
        </select>
      </div>

      <h2>Représentant</h2>
      {["nom_representant","prenom_representant","telephone","adresse"].map((field,i)=>(
        <div className="form-group" key={i}>
          <input
            type={field==="telephone"?"tel":"text"}
            name={field}
            placeholder={field.replace("_"," ").toUpperCase()}
            value={formData[field]}
            onChange={handleChange}
            required
          />
        </div>
      ))}
      <button type="submit">Envoyer</button>
    </form>
  );
}

export default PreinscriptionForm;
