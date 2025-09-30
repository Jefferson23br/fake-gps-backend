from fastapi import APIRouter, Query
import httpx

router = APIRouter()

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"

@router.get("/")
async def get_route(
    origin: str = Query(..., description="Origem no formato 'lon,lat'"),
    destination: str = Query(..., description="Destino no formato 'lon,lat'")
):
    """
    Calcula uma rota entre origem e destino usando OSRM público.
    Exemplo: /route?origin=-46.6543,-23.5632&destination=-46.6430,-23.5678
    """
    url = f"{OSRM_BASE_URL}/{origin};{destination}?overview=full&geometries=geojson"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        return {"error": "Erro ao consultar OSRM", "details": response.text}

    data = response.json()

    # Extrair pontos da rota
    coords = data["routes"][0]["geometry"]["coordinates"]

    return {
        "distance_km": round(data["routes"][0]["distance"] / 1000, 2),
        "duration_min": round(data["routes"][0]["duration"] / 60, 2),
        "points": [{"lon": c[0], "lat": c[1]} for c in coords]
    }