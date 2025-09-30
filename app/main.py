from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import interpolation, simulation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(interpolation.router, prefix="/interpolate")
app.include_router(simulation.router, prefix="/simulate")

@app.get("/")
async def root():
    return {"message": "🚀 Fake GPS Backend is running!"}