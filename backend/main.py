from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import init_db
from routes import eleves, representants

# Initialisation DB
init_db()

app = FastAPI(title="Musique_API", version="1.0.0")

# CORS pour React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routes
app.include_router(eleves.router)
app.include_router(representants.router)

# Page d'accueil API
@app.get("/", summary="Accueil")
def accueil():
    return {"message": "Bienvenue dans l'API Musique"}
