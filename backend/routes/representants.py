from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List
from models import Representant_legal, Eleve
from database import engine

router = APIRouter(prefix="/representants", tags=["Représentants"])

@router.get("/", response_model=List[Representant_legal], summary="Lister tous les représentants")
def lister_representants():
    with Session(engine) as session:
        representants = session.exec(select(Representant_legal)).all()
        if not representants:
            raise HTTPException(status_code=404, detail="Aucun représentant trouvé")
        return representants

@router.get("/{id_representant}", response_model=Representant_legal, summary="Voir un représentant par ID")
def voir_representant(id_representant: int):
    with Session(engine) as session:
        rep = session.get(Representant_legal, id_representant)
        if not rep:
            raise HTTPException(status_code=404, detail="Représentant non trouvé")
        return rep

@router.delete("/{id_representant}", summary="Supprimer un représentant")
def supprimer_representant(id_representant: int):
    with Session(engine) as session:
        rep = session.get(Representant_legal, id_representant)
        if not rep:
            raise HTTPException(status_code=404, detail="Représentant non trouvé")

        enfants_associes = session.exec(select(Eleve).where(Eleve.id_representant == id_representant)).all()
        if enfants_associes:
            raise HTTPException(status_code=400, detail="Impossible de supprimer : des élèves sont encore associés à ce représentant")

        session.delete(rep)
        session.commit()
        return {"detail": f"Représentant {id_representant} supprimé avec succès"}

@router.delete("/", summary="Supprimer tous les représentants")
def supprimer_tous_les_representants():
    with Session(engine) as session:
        eleves = session.exec(select(Eleve)).all()
        if eleves:
            raise HTTPException(status_code=400, detail="Impossible : des élèves sont encore associés à des représentants")

        reps = session.exec(select(Representant_legal)).all()
        if not reps:
            return {"detail": "Aucun représentant à supprimer"}

        for rep in reps:
            session.delete(rep)
        session.commit()
        return {"detail": f"{len(reps)} représentants supprimés avec succès"}
