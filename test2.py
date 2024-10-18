import swisseph as swe
from datetime import datetime
from pytz import timezone
import json
from typing import List, Dict, Tuple

IGING_OFFSET = 58  

# codes from swe-> dict([[i,swe.get_planet_name(i)] for i in range(0,23)])
SWE_PLANET_DICT = {"Sun":0,
                    "Earth":0, # Sun position -180 longitude
                    "Moon":1,
                    "North_Node":11, # Disussion wheater mean or True node?! here North Node -> true Node
                    "South_Node":11, # North_Node position -180 longitude
                    "Mercury":2,
                    "Venus":3,
                    "Mars":4,
                    "Jupiter":5,
                    "Saturn":6,
                    "Uranus":7,
                    "Neptune":8,
                    "Pluto":9,
                   #"Chiron":15,
                   #'Pholus':16,
                   #'Ceres':17,
                   #'Pallas':18,
                   #'Juno':19,
                   #'Vesta':20,
                   }

# Example full_dict from your file (simplified)
full_dict = {
    "full_gate_chakra_dict": {
        64: "HD", 47: "AA",
        61: "HD", 24: "AA",
        63: "HD", 4: "AA",
        17: "AA", 62: "TT",
        43: "AA", 23: "TT",
        11: "AA", 56: "TT",
        16: "TT", 48: "SN",
        20: "TT", 57: "SN",
        # Add more gates and chakras based on GATES_CHAKRA_DICT
    }
}

class Gate:
    def __init__(self, number: int, line: int, color: int, tone: int, base: int):
        self.number = number
        self.line = line
        self.color = color
        self.tone = tone
        self.base = base

class Center:
    def __init__(self, name: str, defined: bool):
        self.name = name
        self.defined = defined

class Chart:
    def __init__(self):
        self.planets = {}
        self.centers = []
        self.gates = {}  # Initialize gates attribute
        self.type = None
        self.authority = None
        self.profile = None

class HumanDesignChart:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, tz_str: str):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.tz_offset = self.get_utc_offset_from_tz(year, month, day, hour, minute, tz_str)

    def get_utc_offset_from_tz(self, year: int, month: int, day: int, hour: int, minute: int, tz_str: str) -> float:
        local_time = datetime(year, month, day, hour, minute)
        tz = timezone(tz_str)
        utc_offset = tz.utcoffset(local_time).total_seconds() / 3600
        return utc_offset

    def calculate_julian_date(self) -> float:
        return swe.julday(self.year, self.month, self.day, self.hour + self.minute / 60 - self.tz_offset)

    def calculate_gates(self, jdut: float) -> Dict[str, Gate]:
        offset = IGING_OFFSET
        gates_info = {}

        for planet_name, planet_code in SWE_PLANET_DICT.items():
            pos = swe.calc_ut(jdut, planet_code)[0][0]
            if planet_name == "Earth":
                pos = (pos + 180) % 360
            angle = (pos + offset) % 360
            gate = int((angle / 360) * 64)
            line = int((angle * 6) % 6 + 1)
            color = int((angle * 6 * 6) % 6 + 1)
            tone = int((angle * 6 * 6 * 6) % 6 + 1)
            base = int((angle * 6 * 6 * 6 * 5) % 5 + 1)
            gates_info[planet_name] = Gate(gate, line, color, tone, base)

        return gates_info

    def generate_chart(self, full_dict: Dict) -> Chart:
        jdut = self.calculate_julian_date()
        gates_info = self.calculate_gates(jdut)

        # Create Chart
        chart = Chart()
        chart.centers = determine_active_centers(gates_info, full_dict)
        chart.type = determine_energy_type(gates_info, chart.centers)
        chart.authority = determine_authority(gates_info, chart.centers)
        chart.profile = determine_profile(gates_info)

        return chart

# Define Energy Type
def determine_energy_type(gates_info: Dict[str, Gate], centers: List[Center]) -> str:
    sacral_defined = any(center.name == "SL" and center.defined for center in centers)
    throat_defined = any(center.name == "TT" and center.defined for center in centers)
    
    motor_centers = ["SL", "HT", "RT", "SP"]  # Sacral, Heart, Root, Solar Plexus
    motor_to_throat = any(
        center.name in motor_centers and center.defined and throat_defined
        for center in centers
    )
    
    if sacral_defined and throat_defined:
        return "Manifesting Generator"
    elif sacral_defined:
        return "Generator"
    elif motor_to_throat:
        return "Manifestor"
    elif throat_defined:
        return "Projector"
    else:
        return "Reflector"

# Define Authority
def determine_authority(gates_info: Dict[str, Gate], centers: List[Center]) -> str:
    if any(center.name == "SP" and center.defined for center in centers):
        return "Emotional"
    elif any(center.name == "SL" and center.defined for center in centers):
        return "Sacral"
    elif any(center.name == "SN" and center.defined for center in centers):
        return "Splenic"
    elif any(center.name == "HT" and center.defined for center in centers):
        return "Ego"
    # Check if both G-Center (GC) and Throat Center (TT) are defined
    elif any(center.name == "GC" and center.defined for center in centers) and \
         any(center.name == "TT" and center.defined for center in centers):
        return "Self-Projected"
    return "None"

# Define Profile
def determine_profile(gates_info: Dict[str, Gate]) -> Tuple[int, int]:
    personality_sun_gate = gates_info.get("Sun").line
    design_sun_gate = gates_info.get("Earth").line  # Earth represents Design
    return personality_sun_gate, design_sun_gate

# Define Active Centers
def determine_active_centers(gates_info: Dict[str, Gate], full_dict) -> List[Center]:
    centers = []
    
    for gate_number in gates_info.values():
        for gate, chakra in full_dict["full_gate_chakra_dict"].items():
            if gate == gate_number.number:
                center_name = chakra
                centers.append(Center(center_name, True))
    
    return centers

# Example function to print chart
def print_hd_chart(chart: Chart) -> str:
    chart_dict = {
        "Energy Type": chart.type,
        "Authority": chart.authority,
        "Profile": f"{chart.profile[0]}/{chart.profile[1]}",
        "Centers": [{"name": center.name, "defined": center.defined} for center in chart.centers],
        "Gates": {planet: {
            "Gate": gate.number, 
            "Line": gate.line, 
            "Color": gate.color, 
            "Tone": gate.tone, 
            "Base": gate.base
        } for planet, gate in chart.gates.items()}
    }
    return json.dumps(chart_dict, indent=4)

if __name__ == "__main__":
#    year = int(input("Enter birth year: "))
#    month = int(input("Enter birth month: "))
#    day = int(input("Enter birth day: "))
#    hour = int(input("Enter birth hour (24h format): "))
#    minute = int(input("Enter birth minute: "))
#    tz_str = input("Enter timezone (e.g., 'Europe/Istanbul'): ")
    year = 1968
    month = 2
    day = 21
    hour = 11
    minute = 00
    tz_str = 'Europe/Istanbul'

    # Generate Human Design Chart
    hd_chart = HumanDesignChart(year, month, day, hour, minute, tz_str)
    chart = hd_chart.generate_chart(full_dict)

    # Print HD Chart in JSON format
    print("Human Design Chart:")
    print(print_hd_chart(chart))
