from fastapi import FastAPI
from app.api.routes import route_calculator, interpolation, simulation

app = FastAPI(
    title="Fake GPS Backend",
    version="0.1.0",
    description="API para gerar rotas, interpolar pontos e simular Fake GPS"
)

# Incluindo rotas
app.include_router(route_calculator.router, prefix="/route", tags=["Route"])
app.include_router(interpolation.router, prefix="/interpolate", tags=["Interpolation"])
app.include_router(simulation.router, prefix="/simulate", tags=["Simulation"])

# Endpoint de teste
@app.get("/")
def root():
    return {"message": "🚀 Fake GPS Backend is running!"}