import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "endpoints" in response.json()
    assert "/geocode" in response.json()["endpoints"]
    assert "/reverse" in response.json()["endpoints"]
    assert "/batch" in response.json()["endpoints"]
    assert "/distance" in response.json()["endpoints"]

@pytest.mark.parametrize("place,expected_bounds", [
    ("New York, USA", {"lat": (40, 41), "lon": (-75, -73)}),
    ("London, UK", {"lat": (51, 52), "lon": (-1, 1)}),
    ("Tokyo, Japan", {"lat": (35, 36), "lon": (139, 140)}),
])
def test_geocode_different_cities(place, expected_bounds):
    test_data = {"place": place}
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["place"] == place
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)
    assert expected_bounds["lat"][0] < data["latitude"] < expected_bounds["lat"][1]
    assert expected_bounds["lon"][0] < data["longitude"] < expected_bounds["lon"][1]
    assert isinstance(data["address"], str)
    assert len(data["address"]) > 0

def test_geocode_with_special_characters():
    test_data = {"place": "München, Germany"}  # City with umlaut
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)
    # Munich coordinates should be roughly around (48.1, 11.5)
    assert 47.5 < data["latitude"] < 48.5
    assert 11 < data["longitude"] < 12

@pytest.mark.parametrize("invalid_place", [
    "ThisPlaceDoesNotExistAnywhere12345",
    "!@#$%^&*()",
])
def test_geocode_nonexistent_places(invalid_place):
    test_data = {"place": invalid_place}
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "Could not find coordinates" in response.json()["detail"]

@pytest.mark.parametrize("invalid_place", [
    "",
    " ",
    "   ",
])
def test_geocode_empty_or_whitespace(invalid_place):
    test_data = {"place": invalid_place}
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 422
    assert "detail" in response.json()
    assert any("Place cannot be empty or whitespace-only" in error["msg"] 
              for error in response.json()["detail"])

def test_geocode_with_coordinates():
    test_data = {"place": "40.7128, -74.0060"}  # New York coordinates
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)
    # Should return coordinates close to input
    assert abs(data["latitude"] - 40.7128) < 0.1
    assert abs(data["longitude"] - (-74.0060)) < 0.1

@pytest.mark.parametrize("invalid_input", [
    {"wrong_field": "New York"},
    {},
    {"place": None},
    {"place": 12345},
    {"place": ["New York"]},
])
def test_geocode_invalid_request_formats(invalid_input):
    response = client.post("/geocode", json=invalid_input)
    assert response.status_code == 422  # FastAPI validation error
    assert "detail" in response.json()

def test_geocode_very_long_place_name():
    # Test with a very long place name (100 characters)
    long_place = "A" * 100
    test_data = {"place": long_place}
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_geocode_with_html_injection():
    test_data = {"place": "<script>alert('xss')</script>"}
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_geocode_with_sql_injection():
    test_data = {"place": "'; DROP TABLE users; --"}
    response = client.post("/geocode", json=test_data)
    assert response.status_code == 404
    assert "detail" in response.json()

# New tests for reverse geocoding
@pytest.mark.parametrize("coords,expected_contains", [
    ((40.7128, -74.0060), "New York"),  # New York
    ((51.5074, -0.1278), "London"),     # London
    ((35.6762, 139.6503), "東京"),      # Tokyo (in Japanese)
])
def test_reverse_geocode_valid_coordinates(coords, expected_contains):
    test_data = {"latitude": coords[0], "longitude": coords[1]}
    response = client.post("/reverse", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["address"], str)
    assert expected_contains in data["address"]
    assert data["latitude"] == coords[0]
    assert data["longitude"] == coords[1]

@pytest.mark.parametrize("invalid_coords", [
    {"latitude": 91, "longitude": 0},    # Invalid latitude
    {"latitude": -91, "longitude": 0},   # Invalid latitude
    {"latitude": 0, "longitude": 181},   # Invalid longitude
    {"latitude": 0, "longitude": -181},  # Invalid longitude
])
def test_reverse_geocode_invalid_coordinates(invalid_coords):
    response = client.post("/reverse", json=invalid_coords)
    assert response.status_code == 422
    assert "detail" in response.json()

# New tests for batch geocoding
def test_batch_geocode_valid_places():
    test_data = {
        "places": ["New York, USA", "London, UK", "Tokyo, Japan"]
    }
    response = client.post("/batch", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(isinstance(item["latitude"], float) for item in data)
    assert all(isinstance(item["longitude"], float) for item in data)
    assert all(isinstance(item["address"], str) for item in data)

def test_batch_geocode_mixed_places():
    test_data = {
        "places": ["New York, USA", "ThisPlaceDoesNotExist123", "London, UK"]
    }
    response = client.post("/batch", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["latitude"] is not None  # New York should be found
    assert data[1]["latitude"] is None      # Invalid place should return None
    assert data[2]["latitude"] is not None  # London should be found

def test_batch_geocode_empty_list():
    test_data = {"places": []}
    response = client.post("/batch", json=test_data)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_batch_geocode_too_many_places():
    test_data = {"places": ["Place " + str(i) for i in range(101)]}  # 101 places
    response = client.post("/batch", json=test_data)
    assert response.status_code == 422
    assert "detail" in response.json()
    assert any("Maximum batch size is 100" in error["msg"] 
              for error in response.json()["detail"])

# New tests for distance calculation
@pytest.mark.parametrize("places,expected_range", [
    (
        {"place1": "New York, USA", "place2": "London, UK"},
        (5000, 6000)  # Roughly 5500 km
    ),
    (
        {"place1": "Paris, France", "place2": "Berlin, Germany"},
        (800, 900)    # Roughly 850 km
    ),
])
def test_distance_calculation(places, expected_range):
    response = client.post("/distance", json=places)
    assert response.status_code == 200
    data = response.json()
    assert data["place1"] == places["place1"]
    assert data["place2"] == places["place2"]
    assert isinstance(data["distance_km"], float)
    assert expected_range[0] < data["distance_km"] < expected_range[1]
    assert data["error"] is None

def test_distance_with_invalid_place():
    test_data = {
        "place1": "New York, USA",
        "place2": "ThisPlaceDoesNotExist123"
    }
    response = client.post("/distance", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["distance_km"] is None
    assert data["error"] is not None
    assert "Could not calculate distance" in data["error"]

def test_distance_with_empty_places():
    test_data = {"place1": "", "place2": "New York, USA"}
    response = client.post("/distance", json=test_data)
    assert response.status_code == 422
    assert "detail" in response.json()
    assert any("Place cannot be empty or whitespace-only" in error["msg"] 
              for error in response.json()["detail"])
