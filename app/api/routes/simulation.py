from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from math import radians, sin, cos, sqrt, atan2

router = APIRouter()

class Point(BaseModel):
    lon: float
    lat: float

class SimulationRequest(BaseModel):
    points: List[Point]
    speed_kmh: float

def haversine(lat1, lon1, lat2, lon2):

    """Distância em metros entre 2 pontos (Haversine)."""

    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2

    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@router.post("/")
def simulate(request: SimulationRequest):
    points = request.points

    speed_mps = request.speed_kmh / 3.6  # km/h → m/s


    speed_mps = request.speed_kmh / 3.6
    if len(points) < 2:
        return {"error": "Precisa de pelo menos 2 pontos"}

    time_offset = 0
    simulated = []