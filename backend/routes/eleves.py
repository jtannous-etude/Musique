from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List, Literal
from datetime import date
from models import Eleve, Activite, Representant_legal
from pydantic import BaseModel, constr
from database import engine

router = APIRouter(prefix="/eleves", tags=["Élèves"])

# -------- Schémas -------- #
class PreinscriptionForm(BaseModel):
    nom_eleve: str
    prenom_eleve: str
    date_naissance: date
    activite: Literal["eveil", "labo", "cursus"]
    nom_representant: str
    prenom_representant: str
    telephone: constr(pattern=r"^\d{10}$")
    adresse: str

class PreinscriptionUpdate(BaseModel):
    nom_eleve: str | None = None
    prenom_eleve: str | None = None
    date_naissance: date | None = None
    activite: Literal["eveil", "labo", "cursus"] | None = None
    nom_representant: str | None = None
    prenom_representant: str | None = None
    telephone: constr(pattern=r"^\d{10}$") | None = None
    adresse: str | None = None

class EleveRead(BaseModel):
    id_eleve: int
    nom: str
    prenom: str
    date_naissance: str
    activite: str
    id_representant: int

    class Config:
        orm_mode = True

# -------- Routes -------- #
@router.post("/", summary="Créer une préinscription")
def creation_preinscription(form: PreinscriptionForm):
    with Session(engine) as session:
        activite = session.exec(select(Activite).where(Activite.nom == form.activite)).first()
        if not activite:
            raise HTTPException(status_code=400, detail="Activité invalide")

        if form.date_naissance > date.today():
            raise HTTPException(status_code=400, detail="Date de naissance invalide")

        rep = session.exec(select(Representant_legal).where(Representant_legal.telephone == form.telephone)).first()
        if not rep:
            rep = Representant_legal(
                nom=form.nom_representant,
                prenom=form.prenom_representant,
                telephone=form.telephone,
                adresse=form.adresse,
            )
            session.add(rep)
            session.commit()
            session.refresh(rep)

        new_eleve = Eleve(
            nom=form.nom_eleve,
            prenom=form.prenom_eleve,
            date_naissance=form.date_naissance,
            id_activite=activite.id_activite,
            id_representant=rep.id_representant,
        )
        session.add(new_eleve)
        session.commit()
        session.refresh(new_eleve)

        return {
            "id_eleve": new_eleve.id_eleve,
            "nom": new_eleve.nom,
            "prenom": new_eleve.prenom,
            "date_naissance": new_eleve.date_naissance.strftime("%d/%m/%Y"),
            "id_representant": rep.id_representant,
            "activite": activite.nom,
        }

@router.get("/", response_model=List[EleveRead])
def lister_preinscriptions():
    with Session(engine) as session:
        eleves = session.exec(select(Eleve)).all()
        result = []
        for e in eleves:
            activite = session.get(Activite, e.id_activite)
            result.append(EleveRead(
                id_eleve=e.id_eleve,
                nom=e.nom,
                prenom=e.prenom,
                date_naissance=e.date_naissance.strftime("%d/%m/%Y"),
                activite=activite.nom,
                id_representant=e.id_representant,
            ))
        return result

@router.get("/{id_eleve}", response_model=EleveRead, summary="Voir une préinscription par ID")
def voir_preinscription(id_eleve: int):
    with Session(engine) as session:
        eleve = session.get(Eleve, id_eleve)
        if not eleve:
            raise HTTPException(status_code=404, detail="Élève non trouvé")
        activite = session.get(Activite, eleve.id_activite)
        return EleveRead(
            id_eleve=eleve.id_eleve,
            nom=eleve.nom,
            prenom=eleve.prenom,
            date_naissance=eleve.date_naissance.strftime("%d/%m/%Y"),
            activite=activite.nom,
            id_representant=eleve.id_representant
        )

@router.put("/{id_eleve}", summary="Mettre à jour une préinscription")
def mise_a_jour_preinscription(id_eleve: int, form: PreinscriptionUpdate):
    with Session(engine) as session:
        eleve = session.get(Eleve, id_eleve)
        if not eleve:
            raise HTTPException(status_code=404, detail="Élève non trouvé")

        if form.nom_eleve:
            eleve.nom = form.nom_eleve
        if form.prenom_eleve:
            eleve.prenom = form.prenom_eleve
        if form.date_naissance:
            if form.date_naissance > date.today():
                raise HTTPException(status_code=400, detail="Date de naissance invalide")
            eleve.date_naissance = form.date_naissance
        if form.activite:
            activite = session.exec(select(Activite).where(Activite.nom == form.activite)).first()
            if not activite:
                raise HTTPException(status_code=400, detail="Activité invalide")
            eleve.id_activite = activite.id_activite

        rep = session.get(Representant_legal, eleve.id_representant)
        if form.nom_representant:
            rep.nom = form.nom_representant
        if form.prenom_representant:
            rep.prenom = form.prenom_representant
        if form.telephone:
            rep.telephone = form.telephone
        if form.adresse:
            rep.adresse = form.adresse

        session.add_all([eleve, rep])
        session.commit()
        return {"detail": f"Élève {id_eleve} mis à jour"}

@router.delete("/{id_eleve}", summary="Supprimer une préinscription")
def suppression_preinscription(id_eleve: int):
    with Session(engine) as session:
        eleve = session.get(Eleve, id_eleve)
        if not eleve:
            raise HTTPException(status_code=404, detail="Élève non trouvé")
        session.delete(eleve)
        session.commit()
        return {"detail": f"Élève {id_eleve} supprimé"}

@router.delete("/", summary="Supprimer tous les élèves")
def supprimer_tous_les_eleves():
    with Session(engine) as session:
        eleves = session.exec(select(Eleve)).all()
        if not eleves:
            return {"detail": "Aucun élève à supprimer"}
        for e in eleves:
            session.delete(e)
        session.commit()
        return {"detail": f"{len(eleves)} élèves supprimés"}
