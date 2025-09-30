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
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@router.post("/")
def simulate(request: SimulationRequest):
    points = request.points
    speed_mps = request.speed_kmh / 3.6  # km/h → m/s
    
    if len(points) < 2:
        return {"error": "Precisa de pelo menos 2 pontos"}

    time_offset = 0
    simulated = []

    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i+1]
        dist = haversine(p1.lat, p1.lon, p2.lat, p2.lon)
        travel_time = dist / speed_mps  # segundos
        simulated.append({"lat": p1.lat, "lon": p1.lon, "time_offset_ms": int(time_offset*1000)})
        time_offset += travel_time

    simulated.append({"lat": points[-1].lat, "lon": points[-1].lon, "time_offset_ms": int(time_offset*1000)})

    return {
        "total_points": len(simulated),
        "total_time_sec": round(time_offset, 2),
        "speed_kmh": request.speed_kmh,
        "route": simulated
    }