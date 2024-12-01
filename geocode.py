from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass

@dataclass
class Location:
    place: str
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str] = None

def get_latitude_longitude(place: str) -> Tuple[Optional[float], Optional[float]]:
    geolocator = Nominatim(user_agent="geocoding_api")
    location = geolocator.geocode(place)
    if location:
        return location.latitude, location.longitude
    return None, None

def get_address(latitude: float, longitude: float) -> Optional[str]:
    """Reverse geocode coordinates to get an address."""
    geolocator = Nominatim(user_agent="geocoding_api")
    try:
        location = geolocator.reverse((latitude, longitude))
        return location.address if location else None
    except:
        return None

def batch_geocode(places: List[str]) -> List[Location]:
    """Geocode multiple places at once."""
    geolocator = Nominatim(user_agent="geocoding_api")
    results = []
    
    for place in places:
        location = geolocator.geocode(place)
        if location:
            results.append(Location(
                place=place,
                latitude=location.latitude,
                longitude=location.longitude,
                address=location.address
            ))
        else:
            results.append(Location(
                place=place,
                latitude=None,
                longitude=None,
                address=None
            ))
    return results

def calculate_distance(place1: str, place2: str) -> Optional[float]:
    """Calculate distance between two places in kilometers."""
    coords1 = get_latitude_longitude(place1)
    coords2 = get_latitude_longitude(place2)
    
    if None in coords1 or None in coords2:
        return None
        
    return geodesic(coords1, coords2).kilometers

place = "Istanbul, Turkey"
latitude, longitude = get_latitude_longitude(place)
print(f"Latitude: {latitude}, Longitude: {longitude}")
