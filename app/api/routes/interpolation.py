from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from math import radians, sin, cos, sqrt, atan2

router = APIRouter()

DISTANCE_STEP = 10  # metros

class Point(BaseModel):
    lon: float
    lat: float

class InterpolationRequest(BaseModel):
    points: List[Point]

def haversine(lat1, lon1, lat2, lon2):
    """Calcula distância em metros entre dois pontos (Haversine)."""
    R = 6371000  # raio da Terra em metros
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def interpolate_points(p1, p2, distance_step=DISTANCE_STEP):
    """Gera pontos intermediários a cada 'distance_step' metros."""
    lat1, lon1 = radians(p1.lat), radians(p1.lon)
    lat2, lon2 = radians(p2.lat), radians(p2.lon)

    total_distance = haversine(p1.lat, p1.lon, p2.lat, p2.lon)
    num_points = int(total_distance // distance_step)

    interpolated = []
    for i in range(1, num_points + 1):
        f = i * distance_step / total_distance
        lat = lat1 + f * (lat2 - lat1)
        lon = lon1 + f * (lon2 - lon1)
        interpolated.append(
            Point(lat=lat * 180.0 / 3.141592653589793,
                  lon=lon * 180.0 / 3.141592653589793)
        )
    return interpolated