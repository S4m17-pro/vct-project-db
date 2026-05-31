import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, jugadores, equipos, partidas, torneos, analytics

app = FastAPI(title="VCT Stats API", description="Backend VCT Stats - Universidad Libre", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(jugadores.router)
app.include_router(equipos.router)
app.include_router(partidas.router)
app.include_router(torneos.router)
app.include_router(analytics.router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "VCT Stats API corriendo"}
