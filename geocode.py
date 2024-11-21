from geopy.geocoders import Nominatim

def get_latitude_longitude(place):
    geolocator = Nominatim(user_agent="your_app")
    location = geolocator.geocode(place)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

place = "Istanbul, Turkey"
latitude, longitude = get_latitude_longitude(place)
print(f"Latitude: {latitude}, Longitude: {longitude}")
