from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Point(BaseModel):
    lat: float
    lon: float
    timestamp: int = 0

class InterpolationRequest(BaseModel):
    points: List[Point]

class InterpolationResponse(BaseModel):
    points: List[Point]

@router.post("/interpolate", response_model=InterpolationResponse)
def interpolate_points(request: InterpolationRequest):
    """
    Gera pontos interpolados entre os pontos recebidos.
    Aqui deixamos simples: apenas replica os pontos originais.
    (Depois podemos colocar lógica para suavizar distâncias/timestamps).
    """
    interpolated_points = []

    for i in range(len(request.points) - 1):
        start = request.points[i]
        end = request.points[i + 1]


        interpolated_points.append(start)


        mid_lat = (start.lat + end.lat) / 2
        mid_lon = (start.lon + end.lon) / 2
        interpolated_points.append(Point(lat=mid_lat, lon=mid_lon, timestamp=start.timestamp + 1))


    interpolated_points.append(request.points[-1])

    return InterpolationResponse(points=interpolated_points)