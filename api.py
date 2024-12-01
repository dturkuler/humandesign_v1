from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, confloat
from typing import Optional, List
from geocode import get_latitude_longitude, get_address, batch_geocode, calculate_distance, Location as GeoLocation

app = FastAPI(
    title="Geocoding API",
    description="An API that converts place names into latitude and longitude coordinates, performs reverse geocoding, and calculates distances",
    version="1.0.0"
)

class LocationRequest(BaseModel):
    place: str

    @field_validator('place')
    @classmethod
    def place_must_not_be_empty_or_whitespace(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Place cannot be empty or whitespace-only")
        return v.strip()

class LocationResponse(BaseModel):
    place: str
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str] = None

class ReverseGeocodeRequest(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)

class BatchGeocodeRequest(BaseModel):
    places: List[str]

    @field_validator('places')
    @classmethod
    def validate_places(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Places list cannot be empty")
        if len(v) > 100:  # Limit batch size
            raise ValueError("Maximum batch size is 100 places")
        return [place.strip() for place in v if place.strip()]

class DistanceRequest(BaseModel):
    place1: str
    place2: str

    @field_validator('place1', 'place2')
    @classmethod
    def validate_place(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Place cannot be empty or whitespace-only")
        return v.strip()

class DistanceResponse(BaseModel):
    place1: str
    place2: str
    distance_km: Optional[float]
    error: Optional[str] = None

@app.post("/geocode", response_model=LocationResponse)
async def geocode_place(request: LocationRequest):
    latitude, longitude = get_latitude_longitude(request.place)
    
    if latitude is None or longitude is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find coordinates for place: {request.place}"
        )
    
    address = get_address(latitude, longitude)
    return LocationResponse(
        place=request.place,
        latitude=latitude,
        longitude=longitude,
        address=address
    )

@app.post("/reverse", response_model=LocationResponse)
async def reverse_geocode(request: ReverseGeocodeRequest):
    address = get_address(request.latitude, request.longitude)
    if not address:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find address for coordinates: ({request.latitude}, {request.longitude})"
        )
    
    return LocationResponse(
        place=f"{request.latitude}, {request.longitude}",
        latitude=request.latitude,
        longitude=request.longitude,
        address=address
    )

@app.post("/batch", response_model=List[LocationResponse])
async def batch_geocode_places(request: BatchGeocodeRequest):
    results = batch_geocode(request.places)
    return [
        LocationResponse(
            place=loc.place,
            latitude=loc.latitude,
            longitude=loc.longitude,
            address=loc.address
        ) for loc in results
    ]

@app.post("/distance", response_model=DistanceResponse)
async def get_distance(request: DistanceRequest):
    distance = calculate_distance(request.place1, request.place2)
    if distance is None:
        return DistanceResponse(
            place1=request.place1,
            place2=request.place2,
            distance_km=None,
            error="Could not calculate distance. One or both places not found."
        )
    
    return DistanceResponse(
        place1=request.place1,
        place2=request.place2,
        distance_km=round(distance, 2)
    )

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Geocoding API",
        "endpoints": {
            "/geocode": "Convert a place name to coordinates (POST)",
            "/reverse": "Convert coordinates to an address (POST)",
            "/batch": "Geocode multiple places at once (POST)",
            "/distance": "Calculate distance between two places (POST)"
        }
    }
