from sqlmodel import SQLModel, create_engine
from pathlib import Path
import json
from models import Activite, Eleve, Representant_legal

DATABASE_URL = "sqlite:///./musique.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

    # Charger activités depuis JSON
    json_file = Path(__file__).parent / "data" / "activites.json"
    with open(json_file, "r", encoding="utf-8") as f:
        activites = json.load(f)

    from sqlmodel import Session, select
    with Session(engine) as session:
        for act in activites:
            exists = session.exec(select(Activite).where(Activite.nom == act["nom"])).first()
            if not exists:
                session.add(Activite(nom=act["nom"]))
        session.commit()
