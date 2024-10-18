import swisseph as swe
from datetime import datetime
import json
from typing import Dict, List, Tuple, Union
import unittest
import math

class Planet:
    def __init__(self, name: str, longitude: float):
        self.name = name
        self.longitude = longitude

class Gate:
    def __init__(self, number: int, line: int):
        self.number = number
        self.line = line

class Center:
    def __init__(self, name: str, defined: bool):
        self.name = name
        self.defined = defined

class Channel:
    def __init__(self, start_gate: int, end_gate: int):
        self.start_gate = start_gate
        self.end_gate = end_gate

class HumanDesignChart:
    def __init__(self, dob: str, tob: str, pob: str):
        self.dob = dob
        self.tob = tob
        self.pob = pob
        self.planets: List[Planet] = []
        self.gates: List[Gate] = []
        self.centers: List[Center] = []
        self.channels: List[Channel] = []
        self.energy_type = ""
        self.authority = ""
        self.profile = ""
        self.strategy = ""

    def calculate_chart(self) -> None:
        birth_datetime = datetime.strptime(f"{self.dob} {self.tob}", "%Y-%m-%d %H:%M")
        julian_day = swe.julday(birth_datetime.year, birth_datetime.month, birth_datetime.day, 
                                birth_datetime.hour + birth_datetime.minute / 60)
        
        # Calculate planetary positions
        planets = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, 
                   swe.URANUS, swe.NEPTUNE, swe.PLUTO, swe.MEAN_NODE]
        planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", 
                        "Uranus", "Neptune", "Pluto", "North Node"]
        
        for planet, name in zip(planets, planet_names):
            longitude, _ = swe.calc_ut(julian_day, planet)[0:2]
            self.planets.append(Planet(name, longitude))
        
        # Calculate gates and channels
        self.calculate_gates()
        self.calculate_channels()
        
        # Determine centers
        self.determine_centers()

    def calculate_gates(self) -> None:
        for planet in self.planets:
            gate_number = math.floor((planet.longitude % 360) / 5.625) + 1
            line_number = math.floor(((planet.longitude % 360) % 5.625) / 0.9375) + 1
            self.gates.append(Gate(gate_number, line_number))

    def calculate_channels(self) -> None:
        channel_definitions = [
            (1, 8), (2, 14), (3, 60), (4, 63), (5, 15), (6, 59), (7, 31), (9, 52), (10, 20),
            (11, 56), (12, 22), (13, 33), (16, 48), (17, 62), (18, 58), (19, 49), (20, 57),
            (21, 45), (23, 43), (24, 61), (25, 51), (26, 44), (27, 50), (28, 38), (29, 46),
            (30, 41), (32, 54), (34, 57), (35, 36), (37, 40), (39, 55), (42, 53), (47, 64)
        ]
        
        active_gates = set(gate.number for gate in self.gates)
        for start, end in channel_definitions:
            if start in active_gates and end in active_gates:
                self.channels.append(Channel(start, end))

    def determine_centers(self) -> None:
        center_definitions = {
            "Head": [64, 61, 63, 47, 24, 4],
            "Ajna": [47, 24, 4, 17, 43, 11],
            "Throat": [62, 23, 56, 35, 8, 31, 33, 7, 45, 12],
            "G": [15, 2, 46, 25, 10],
            "Heart": [21, 40, 26, 51],
            "Solar Plexus": [30, 36, 55, 37, 6, 22],
            "Sacral": [5, 14, 29, 59, 9, 3, 42, 27],
            "Spleen": [48, 57, 44, 50, 32, 28, 18],
            "Root": [58, 38, 54, 53, 60, 52, 19, 39]
        }
        
        active_gates = set(gate.number for gate in self.gates)
        for center, gates in center_definitions.items():
            is_defined = any(gate in active_gates for gate in gates)
            self.centers.append(Center(center, is_defined))

    def determine_energy_type(self) -> None:
        defined_centers = [center.name for center in self.centers if center.defined]
        
        if "Sacral" in defined_centers:
            if "Heart" in defined_centers and "Solar Plexus" in defined_centers:
                self.energy_type = "Manifesting Generator"
            else:
                self.energy_type = "Generator"
        elif "Solar Plexus" in defined_centers:
            self.energy_type = "Manifestor"
        elif "Spleen" in defined_centers:
            self.energy_type = "Projector"
        else:
            self.energy_type = "Reflector"

    def determine_authority(self) -> None:
        defined_centers = [center.name for center in self.centers if center.defined]
        
        if "Solar Plexus" in defined_centers:
            self.authority = "Emotional"
        elif "Sacral" in defined_centers:
            self.authority = "Sacral"
        elif "Spleen" in defined_centers:
            self.authority = "Splenic"
        elif "Heart" in defined_centers:
            self.authority = "Ego"
        elif "G" in defined_centers:
            self.authority = "Self-Projected"
        else:
            self.authority = "Mental"

    def determine_profile(self) -> None:
        personality_sun = next(gate for gate in self.gates if gate.number == self.planets[0].number)
        design_sun = next(gate for gate in self.gates if gate.number == self.planets[1].number)
        
        self.profile = f"{personality_sun.line}/{design_sun.line}"

    def determine_strategy(self) -> None:
        strategies = {
            "Generator": "To Respond",
            "Manifesting Generator": "To Respond, then Inform",
            "Manifestor": "To Inform",
            "Projector": "To Wait for the Invitation",
            "Reflector": "To Wait a Lunar Cycle"
        }
        self.strategy = strategies.get(self.energy_type, "Unknown")

    def to_dict(self) -> Dict[str, Union[str, List[Dict[str, Union[str, int, float, bool]]]]]:
        return {
            "birth_data": {
                "date": self.dob,
                "time": self.tob,
                "place": self.pob
            },
            "energy_type": self.energy_type,
            "authority": self.authority,
            "profile": self.profile,
            "strategy": self.strategy,
            "planets": [{"name": p.name, "longitude": p.longitude} for p in self.planets],
            "gates": [{"number": g.number, "line": g.line} for g in self.gates],
            "centers": [{"name": c.name, "defined": c.defined} for c in self.centers],
            "channels": [{"start_gate": c.start_gate, "end_gate": c.end_gate} for c in self.channels]
        }

def validate_input(dob: str, tob: str, pob: str) -> Tuple[bool, str]:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        datetime.strptime(tob, "%H:%M")
        if not isinstance(pob, str) or "," not in pob:
            raise ValueError("Invalid place of birth format")
    except ValueError as e:
        return False, str(e)
    return True, ""

def generate_human_design_chart(dob: str, tob: str, pob: str) -> Dict[str, Union[str, List[Dict[str, Union[str, int, float, bool]]]]]:
    is_valid, error_message = validate_input(dob, tob, pob)
    if not is_valid:
        raise ValueError(f"Invalid input: {error_message}")

    chart = HumanDesignChart(dob, tob, pob)
    chart.calculate_chart()
    chart.determine_energy_type()
    chart.determine_authority()
    chart.determine_profile()
    chart.determine_strategy()

    return chart.to_dict()

class TestHumanDesignChart(unittest.TestCase):
    def test_input_validation(self):
        self.assertTrue(validate_input("2000-01-01", "12:00", "New York, USA")[0])
        self.assertFalse(validate_input("2000-01-01", "25:00", "New York, USA")[0])
        self.assertFalse(validate_input("2000-01-01", "12:00", "Invalid")[0])

    def test_chart_generation(self):
        chart_data = generate_human_design_chart("2000-01-01", "12:00", "New York, USA")
        self.assertIsInstance(chart_data, dict)
        self.assertIn("energy_type", chart_data)
        self.assertIn("authority", chart_data)
        self.assertIn("profile", chart_data)
        self.assertIn("strategy", chart_data)

if __name__ == "__main__":
    # Run unit tests
    unittest.main(argv=[''], exit=False)

    # User input section
    DOB = "1990-05-15"
    TOB = "14:30"
    POB = "London, UK"

    try:
        chart_data = generate_human_design_chart(DOB, TOB, POB)
        print(json.dumps(chart_data, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
