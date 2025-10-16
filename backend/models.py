from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field
from typing import Literal

class Activite(SQLModel, table=True):
    id_activite: Optional[int] = Field(default=None, primary_key=True)
    nom: str

class Representant_legal(SQLModel, table=True):
    id_representant: Optional[int] = Field(default=None, primary_key=True)
    telephone: str
    nom: str
    prenom: str
    adresse: str

class Eleve(SQLModel, table=True):
    id_eleve: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    date_naissance: date
    id_activite: int
    id_representant: int
