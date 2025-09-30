from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import simulation, interpolation, route_calculator

app = FastAPI(title="Fake GPS Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Inclui as rotas
app.include_router(route_calculator.router, prefix="/route", tags=["route"])
app.include_router(interpolation.router, prefix="/interpolate", tags=["interpolation"])
app.include_router(simulation.router, prefix="/simulate", tags=["simulation"])

# 🔹 Rota raiz
@app.get("/")
async def root():
    return {"status": "🚀 Fake GPS Backend is running!"}