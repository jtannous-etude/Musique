from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class Activite(SQLModel, table=True):
    id_activite: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(max_length=100)

class Activite_create(SQLModel):
    nom: str

class Activite_read(SQLModel):
    id_activite: int
    nom: str

class Representant_legal(SQLModel, table=True):
    id_representant: Optional[int] = Field(default=None, primary_key=True)
    telephone: str = Field(max_length=10, unique=True)
    nom: str
    prenom: str
    adresse: str

class Representant_legal_create(SQLModel):
    telephone: str
    nom: str
    prenom: str
    adresse: str

class Eleve(SQLModel, table=True):
    id_eleve: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    date_naissance: date
    id_activite: int = Field(foreign_key="activite.id_activite")
    id_representant: int = Field(foreign_key="representant_legal.id_representant")

class Eleve_create(SQLModel):
    nom: str
    prenom: str
    date_naissance: date
    id_activite: int
    id_representant: int
