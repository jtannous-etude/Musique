from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from models import Activite, Activite_create, Representant_legal, Representant_legal_create, Eleve, Eleve_create
from pydantic import BaseModel
from datetime import date
from typing import Literal

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

app = FastAPI()

# CORS pour React
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# --- Activites ---
@app.post("/activites/", response_model=Activite_create)
def create_activite(activite: Activite_create):
    db_activite = Activite(nom=activite.nom)
    with Session(engine) as session:
        session.add(db_activite)
        session.commit()
        session.refresh(db_activite)
    return db_activite

@app.get("/activites/")
def read_activites():
    with Session(engine) as session:
        return session.exec(select(Activite)).all()

# --- Representants ---
@app.post("/representants/", response_model=Representant_legal_create)
def create_representant(rep: Representant_legal_create):
    db_rep = Representant_legal(**rep.dict())
    with Session(engine) as session:
        session.add(db_rep)
        session.commit()
        session.refresh(db_rep)
    return db_rep

@app.get("/representants/")
def read_representants():
    with Session(engine) as session:
        return session.exec(select(Representant_legal)).all()

# --- Eleves ---
@app.post("/eleves/", response_model=Eleve_create)
def create_eleve(eleve: Eleve_create):
    db_eleve = Eleve(**eleve.dict())
    with Session(engine) as session:
        session.add(db_eleve)
        session.commit()
        session.refresh(db_eleve)
    return db_eleve

@app.get("/eleves/")
def read_eleves():
    with Session(engine) as session:
        return session.exec(select(Eleve)).all()

# --- Preinscription ---
class Preinscription(BaseModel):
    nom_eleve: str
    prenom_eleve: str
    date_naissance: date
    activite: Literal["eveil", "labo", "cursus"]
    nom_representant: str
    prenom_representant: str
    telephone: str
    adresse: str

@app.post("/preinscriptions/")
def create_preinscription(pre: Preinscription):
    with Session(engine) as session:
        rep = session.exec(select(Representant_legal).where(Representant_legal.telephone==pre.telephone)).first()
        if not rep:
            rep = Representant_legal(
                nom=pre.nom_representant,
                prenom=pre.prenom_representant,
                telephone=pre.telephone,
                adresse=pre.adresse
            )
            session.add(rep)
            session.commit()
            session.refresh(rep)
        
        act = session.exec(select(Activite).where(Activite.nom==pre.activite)).first()
        if not act:
            act = Activite(nom=pre.activite)
            session.add(act)
            session.commit()
            session.refresh(act)
        
        eleve = Eleve(
            nom=pre.nom_eleve,
            prenom=pre.prenom_eleve,
            date_naissance=pre.date_naissance,
            id_activite=act.id_activite,
            id_representant=rep.id_representant
        )
        session.add(eleve)
        session.commit()
        session.refresh(eleve)
        return {"message": "Préinscription ajoutée", "id_eleve": eleve.id_eleve}
