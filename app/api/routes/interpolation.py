from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from math import radians, cos, sin, asin, sqrt

router = APIRouter()

class Point(BaseModel):
    lat: float
    lon: float
    timestamp: float = 0  

class InterpolationRequest(BaseModel):
    points: List[Point]
    speed_kmh: float = 60.0  

class InterpolationResponse(BaseModel):
    points: List[Point]


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


def interpolate_segment(start: Point, end: Point, step_meters: int, speed_ms: float, base_time: float):
    dist = haversine(start.lat, start.lon, end.lat, end.lon)
    if dist == 0:
        return [Point(lat=start.lat, lon=start.lon, timestamp=base_time)], 0.0

    num_points = int(dist // step_meters)
    points = []
    total_elapsed = 0.0

    for i in range(num_points + 1):
        frac = i / num_points if num_points > 0 else 1
        lat = start.lat + (end.lat - start.lat) * frac
        lon = start.lon + (end.lon - start.lon) * frac
        elapsed = frac * dist 
        timestamp = base_time + (elapsed / speed_ms)
        points.append(Point(lat=lat, lon=lon, timestamp=timestamp))

    return points, dist / speed_ms  


@router.post("/interpolate", response_model=InterpolationResponse)
def interpolate_points(request: InterpolationRequest, step_meters: int = 10):
    """
    Interpola pontos a cada X metros (padrão 10m) e
    adiciona timestamp em segundos baseado na velocidade (km/h).
    """
    speed_ms = request.speed_kmh * 1000 / 3600 
    interpolated_points = []
    total_time = 0.0

    for i in range(len(request.points) - 1):
        start = request.points[i]
        end = request.points[i + 1]

        segment_points, elapsed_time = interpolate_segment(start, end, step_meters, speed_ms, total_time)

        if interpolated_points and segment_points:
            segment_points = segment_points[1:]

        interpolated_points.extend(segment_points)
        total_time += elapsed_time

    return InterpolationResponse(points=interpolated_points)