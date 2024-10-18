import ephem
from datetime import datetime
import json
import numpy as np
from geopy.geocoders import Nominatim
from dateutil.relativedelta import relativedelta


class Planet:
    def __init__(self, name, ephem_planet):
        self.name = name
        self.ephem_planet = ephem_planet

class Gate:
    def __init__(self, number, name):
        self.number = number
        self.name = name

class Center:
    def __init__(self, name, defined):
        self.name = name
        self.defined = defined

class HumanDesignChart:
    SWE_PLANET_DICT = {"Sun": ephem.Sun(), "Moon": ephem.Moon(), 
                       "Mercury": ephem.Mercury(), "Venus": ephem.Venus(), 
                       "Mars": ephem.Mars(), "Jupiter": ephem.Jupiter(), 
                       "Saturn": ephem.Saturn(), "Uranus": ephem.Uranus(), 
                       "Neptune": ephem.Neptune(), "Pluto": ephem.Pluto()}

    def __init__(self, dob, tob, pob):
        self.dob = dob
        self.tob = tob
        self.pob = self.geocode_pob(pob)  # Use geopy to get lat/lon
        self.planets = self.init_planets()
        self.gates = self.init_gates()
        self.centers = self.init_centers()
        self.IGING_CIRCLE_LIST = [41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3, 27, 24, 2, 23, 8, 
                      20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 
                      46, 18, 48, 57, 32, 50, 28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60]
        self.SWE_PLANET_DICT = {"Sun": ephem.Sun(), "Moon": ephem.Moon(), 
                                 "Mercury": ephem.Mercury(), "Venus": ephem.Venus(), 
                                 "Mars": ephem.Mars(), "Jupiter": ephem.Jupiter(), 
                                 "Saturn": ephem.Saturn(), "Uranus": ephem.Uranus(), 
                                 "Neptune": ephem.Neptune(), "Pluto": ephem.Pluto()}
        self.CHAKRA_LIST = ["HD","AA","TT","GC","HT","SP","SN","SL","RT"]
        self.GATES_CHAKRA_DICT = {(64,47):("HD","AA"), (61,24):("HD","AA"), (63, 4):("HD","AA"), 
                                  (17,62):("AA","TT"), (43,23):("AA","TT"), (11,56):("AA","TT"), 
                                  (16,48):("TT","SN"), (20,57):("TT","SN"), (20,34):("TT","SL"), 
                                  (31, 7):("TT","GC"), ( 8, 1):("TT","GC"), (33,13):("TT","GC"), 
                                  (45,21):("TT","HT"), (35,36):("TT","SP"), (12,22):("TT","SP"), 
                                  (32,54):("SN","RT"), (28,38):("SN","RT"), (57,34):("SN","SL"), 
                                  (50,27):("SN","SL"), (18,58):("SN","RT"), (10,34):("GC","SL"), 
                                  (15, 5):("GC","SL"), ( 2,14):("GC","SL"), (46,29):("GC","SL"), 
                                  (10,57):("GC","SN"), (25,51):("GC","HT"), (59, 6):("SL","SP"), 
                                  (42,53):("SL","RT"), ( 3,60):("SL","RT"), ( 9,52):("SL","RT"), 
                                  (26,44):("HT","SN"), (40,37):("HT","SP"), (49,19):("SP","RT"), 
                                  (55,39):("SP","RT"), (30,41):("SP","RT")}
        self.IC_CROSS_TYP = { (1,3):"RAC", (1,4):"RAC", (2,4):"RAC", (2,5):"RAC", (3,5):"RAC", 
                              (3,6):"RAC", (4,6):"RAC", (4,1):"JXP", (5,1):"LAC", (5,2):"LAC", 
                              (6,2):"LAC", (6,3):"LAC",}

    def init_planets(self):
        return {
            "Sun": Planet("Sun", self.SWE_PLANET_DICT["Sun"]),
            "Moon": Planet("Moon", self.SWE_PLANET_DICT["Moon"]),
            "Mercury": Planet("Mercury", self.SWE_PLANET_DICT["Mercury"]),
            "Venus": Planet("Venus", self.SWE_PLANET_DICT["Venus"]),
            "Mars": Planet("Mars", self.SWE_PLANET_DICT["Mars"]),
            "Jupiter": Planet("Jupiter", self.SWE_PLANET_DICT["Jupiter"]),
            "Saturn": Planet("Saturn", self.SWE_PLANET_DICT["Saturn"]),
            "Uranus": Planet("Uranus", self.SWE_PLANET_DICT["Uranus"]),
            "Neptune": Planet("Neptune", self.SWE_PLANET_DICT["Neptune"]),
            "Pluto": Planet("Pluto", self.SWE_PLANET_DICT["Pluto"]),
        }

    def init_gates(self):
        gates = {}
        for i in range(1, 65):
            gates[i] = Gate(i, f"Gate {i}")
        return gates

    def init_centers(self):
        return {
            "Crown": Center("Crown", False),
            "Ajna": Center("Ajna", False),
            "Throat": Center("Throat", False),
            "G": Center("G", False),
            "Heart": Center("Heart", False),
            "Spleen": Center("Spleen", False),
            "Sacral": Center("Sacral", False),
            "Root": Center("Root", False)
        }

    def geocode_pob(self, pob):
        geolocator = Nominatim(user_agent="human_design_chart")
        location = geolocator.geocode(pob)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError("Unable to geocode Place of Birth. Please check the format (e.g., 'City, Country').")

    def calculate_chart(self):
        observer = ephem.Observer()
        observer.lat = str(self.pob[0])  # Get latitude from geocoded POB
        observer.lon = str(self.pob[1])  # Get longitude from geocoded POB

        # Calculate planetary positions for birth date
        observer.date = datetime(self.dob.year, self.dob.month, self.dob.day, self.tob.hour, self.tob.minute)
        planetary_positions = self.calculate_planetary_positions(observer)

        # Calculate planetary positions for create date
        create_date = self.calculate_create_date(planetary_positions)
        observer.date = create_date
        create_planetary_positions = self.calculate_planetary_positions(observer)

        birth_gate_dict = self.date_to_gate(planetary_positions, "Birth")
        create_gate_dict = self.date_to_gate(create_planetary_positions, "Create")
        date_to_gate_dict = self.birth_creat_date_to_gate(birth_gate_dict, create_gate_dict)

        energy_type = self.get_typ(date_to_gate_dict, self.get_active_chakras(date_to_gate_dict))
        authority = self.get_auth(self.get_active_chakras(date_to_gate_dict), self.get_active_channels(date_to_gate_dict))
        defined_centers = self.get_defined_centers(self.get_active_chakras(date_to_gate_dict))
        profile = self.get_profile(date_to_gate_dict)
        strategy = self.get_strategy(energy_type)
        active_gates, active_channels = self.get_active_gates_and_channels(date_to_gate_dict)

        chart = {
            "Energy Type": energy_type,
            "Authority": authority,
            "Defined Centers": defined_centers,
            "Profile": profile,
            "Strategy": strategy,
            "Active Gates": active_gates,
            "Active Channels": active_channels,
            "Planetary Positions": planetary_positions,
            "Date to Gate": date_to_gate_dict
        }

        return chart

    def calculate_planetary_positions(self, observer):
        planetary_positions = {}
        for planet in self.planets.values():
            observer.date = datetime(self.dob.year, self.dob.month, self.dob.day, self.tob.hour, self.tob.minute)
            planet.ephem_planet.compute(observer)
            planetary_positions[planet.name] = planet.ephem_planet.ra  # Use right ascension as position
        return planetary_positions


    def calculate_create_date(self, planetary_positions):
        # For simplicity, assume the create date is 3 months before the birth date
        create_date = self.dob - relativedelta(months=3)
        
        # Ensure the time remains the same (hour and minute)
        create_date = create_date.replace(hour=self.tob.hour, minute=self.tob.minute)
        
        return create_date


    def date_to_gate(self, planetary_positions, label):
        offset = 58  # synchronize IGING and zodiac circle
        result_dict = {k: [] 
                       for k in ["label", "planets", "lon", "gate", "line", "color", "tone", "base"]
                      }

        for idx,(planet,planet_position) in enumerate(planetary_positions.items()):
            angle = (planet_position + offset) % 360 
            angle_percentage = angle/360 
            
            # convert angle to gate,line,color,tone,base
            gate = self.IGING_CIRCLE_LIST[int(angle_percentage*64)] 
            line = int((angle_percentage*64*6)%6+1)
            color =int((angle_percentage*64*6*6)%6+1)
            tone =int((angle_percentage*64*6*6*6)%6+1)
            base =int((angle_percentage*64*6*6*6*5)%5+1)

            result_dict["label"].append(label)
            result_dict["planets"].append(planet)
            result_dict["lon"].append(planet_position)
            result_dict["gate"].append(gate)
            result_dict["line"].append(line)
            result_dict["color"].append(color)
            result_dict["tone"].append(tone)
            result_dict["base"].append(base)
            
        return result_dict

    def birth_creat_date_to_gate(self, birth_gate_dict, create_gate_dict):
        date_to_gate_dict = {
            key: birth_gate_dict[key] + create_gate_dict[key] 
            for key in birth_gate_dict.keys()
                            }
        return date_to_gate_dict

    def get_typ(self, date_to_gate_dict, active_chakras):
        # No active centers => Reflector
        if len(active_chakras) == 0:
            return "Reflector"
        
        # Case: Sacral is undefined (can be Manifestor or Projector)
        if "SL" not in active_chakras:
            # If Throat is undefined, it must be a Projector
            if "TT" not in active_chakras:
                return "Projector"

            # Check connections from motor centers (HT, EM, RT) to throat (=> Manifestor)
            component = self.get_component(self.get_active_channels(date_to_gate_dict), "TT")  
            if "HT" in active_chakras and self.get_component(self.get_active_channels(date_to_gate_dict), "HT") == component:
                return "Manifestor"
            if "EM" in active_chakras and self.get_component(self.get_active_channels(date_to_gate_dict), "EM") == component:
                return "Manifestor"
            if "RT" in active_chakras and self.get_component(self.get_active_channels(date_to_gate_dict), "RT") == component:
                return "Manifestor"
            
            # If no motor center is connected to the throat, it is a Projector by definition
            return "Projector"
        
        # Case: Sacral is defined (can be Generator or Manifesting Generator)
        if "TT" not in active_chakras:
            return "Generator"

        # Check connections from motor centers (HT, EM, RT) to throat (=> Manifesting Generator)
        if "HT" in active_chakras and self.get_component(self.get_active_channels(date_to_gate_dict), "HT") == self.get_component(self.get_active_channels(date_to_gate_dict), "TT"):
            return "Manifesting Generator"
        if "EM" in active_chakras and self.get_component(self.get_active_channels(date_to_gate_dict), "EM") == self.get_component(self.get_active_channels(date_to_gate_dict), "TT"):
            return "Manifesting Generator"
        if "RT" in active_chakras and self.get_component(self.get_active_channels(date_to_gate_dict), "RT") == self.get_component(self.get_active_channels(date_to_gate_dict), "TT"):
            return "Manifesting Generator"
        if self.get_component(self.get_active_channels(date_to_gate_dict), "SL") == self.get_component(self.get_active_channels(date_to_gate_dict), "TT"):
            return "Manifesting Generator"

        # No connection to throat => Generator
        return "Generator"

    def get_component(self, active_channels_dict, chakra):
        return active_channels_dict.get(chakra, None)

    def get_auth(self, active_chakras, active_channels_dict): 
        outher_auth_mask = (("HD" in active_chakras) 
                            | ("AA" in active_chakras) 
                            | ("TT" in active_chakras)
                            | (len(active_chakras)==0)
                           )
        if "SP" in active_chakras:
            auth = "SP"
        elif "SL" in active_chakras:
            auth = "SL"
        elif "SN" in active_chakras:
            auth = "SN"
        elif (self.is_connected(active_channels_dict,"HT","TT")): 
            auth= "HT"
        elif (self.is_connected(active_channels_dict,"GC","TT")): 
            auth = "GC"
        elif ("GC" in active_chakras) & ("HT" in active_chakras):
            auth = "HT_GC"
        elif outher_auth_mask:
            auth = "outher_auth"
        else: auth = "unknown?" 
        
        return auth

    def is_connected(self, active_channels_dict, *args):
        gate_chakra_list = active_channels_dict["gate_chakra"]
        ch_gate_chakra_list = active_channels_dict["ch_gate_chakra"]
        
        for arg in args:
            if arg not in gate_chakra_list and arg not in ch_gate_chakra_list:
                return False
                
        gate_chakra_set = set(gate_chakra_list)
        ch_gate_chakra_set = set(ch_gate_chakra_list)
        arg_set = set(args)
        
        intersection_gate = gate_chakra_set.intersection(arg_set)
        intersection_ch_gate = ch_gate_chakra_set.intersection(arg_set)
        
        # Check if all arguments are connected
        return len(intersection_gate) + len(intersection_ch_gate) == len(arg_set)

    def get_active_chakras(self, date_to_gate_dict):
        active_chakras = set()
        gate_list =  date_to_gate_dict["gate"]
        ch_gate_list=[0]*len(date_to_gate_dict["gate"])
        
        full_dict = self.full_dict()
        ch_gate_a = full_dict["full_gate_1_list"]
        ch_gate_b = full_dict["full_gate_2_list"]
        for idx,gate in enumerate(gate_list):

            gate_index=np.where(
                np.array(ch_gate_a)==gate
            )
            ch_gate = [ch_gate_b[index] 
                    for index in gate_index[0] 
                    if ch_gate_b[index] in gate_list
                    ]      
            if ch_gate:
                ch_gate_list[idx] = ch_gate[0] 
                active_chakras.add(
                    full_dict["full_chakra_1_list"]
                    [full_dict["full_gate_1_list"].index(gate)]
                )
                active_chakras.add(
                    full_dict["full_chakra_2_list"]
                    [full_dict["full_gate_2_list"].index(gate)]
                ) 
        return active_chakras

    def get_active_channels(self, date_to_gate_dict):
        active_channels_dict={}
        gate_list =  date_to_gate_dict["gate"]
        ch_gate_list=[0]*len(date_to_gate_dict["gate"])
        
        full_dict = self.full_dict()
        ch_gate_a = full_dict["full_gate_1_list"]
        ch_gate_b = full_dict["full_gate_2_list"]
        for idx,gate in enumerate(gate_list):

            gate_index=np.where(
                np.array(ch_gate_a)==gate
            )
            ch_gate = [ch_gate_b[index] 
                    for index in gate_index[0] 
                    if ch_gate_b[index] in gate_list
                    ]      
            if ch_gate:
                ch_gate_list[idx] = ch_gate[0] 
                    
        date_to_gate_dict["ch_gate"]=ch_gate_list

        mask=np.array(date_to_gate_dict["ch_gate"])!=0
        
        for key in ["gate","ch_gate"]: 
            active_channels_dict[key] = np.array(date_to_gate_dict[key])[mask]   
        active_channels_dict["gate_chakra"] =  [full_dict["full_gate_chakra_dict"][key] 
                                                for key in active_channels_dict["gate"]]
        active_channels_dict["ch_gate_chakra"] =  [full_dict["full_gate_chakra_dict"][key] 
                                                for key in active_channels_dict["ch_gate"]]
            
        return active_channels_dict

    def get_strategy(self, energy_type):
        if energy_type == "Generator":
            return "Respond to Life"
        elif energy_type == "Manifestor":
            return "Initiate and Inform"
        elif energy_type == "Manifesting Generator":
            return "Respond and Initiate"
        elif energy_type == "Projector":
            return "Wait for Invitation"
        elif energy_type == "Reflector":
            return "Wait for Invitation and Reflect"

    def get_profile(self, date_to_gate_dict):
        df = date_to_gate_dict
        idx = int(len(df["line"])/2) 
        profile = (df["line"][0],df["line"][idx]) 
        if profile not in self.IC_CROSS_TYP.keys():
            profile = profile[::-1]
        
        return profile

    def get_defined_centers(self, active_chakras):
        defined_centers = []
        for chakra in self.CHAKRA_LIST:
            if chakra in active_chakras:
                defined_centers.append(chakra)
        return defined_centers

    def get_active_gates_and_channels(self, date_to_gate_dict):
        active_gates, active_channels = [], []
        gate_list =  date_to_gate_dict["gate"]
        ch_gate_list=[0]*len(date_to_gate_dict["gate"])
        
        full_dict = self.full_dict()
        ch_gate_a = full_dict["full_gate_1_list"]
        ch_gate_b = full_dict["full_gate_2_list"]
        for idx,gate in enumerate(gate_list):

            gate_index=np.where(
                np.array(ch_gate_a)==gate
            )
            ch_gate = [ch_gate_b[index] 
                    for index in gate_index[0] 
                    if ch_gate_b[index] in gate_list
                    ]      
            if ch_gate:
                ch_gate_list[idx] = ch_gate[0] 
                active_gates.append(gate)
                active_channels.append(f"{gate} - {ch_gate[0]}")
            
        return active_gates, active_channels
    
    def full_dict(self):
        cols = ["full_ch_chakra_list", "full_ch_list", "full_ch_gates_chakra_dict", 
                 "full_chakra_1_list", "full_chakra_2_list", "full_gate_1_list", "full_gate_2_list", "full_gate_chakra_dict"]
        
        full_dict = {k: [] for k in cols}
        
        full_dict["full_ch_chakra_list"] = list(self.GATES_CHAKRA_DICT.values()) + [item[::-1] for item in self.GATES_CHAKRA_DICT.values()]
        full_dict["full_ch_list"] = list(self.GATES_CHAKRA_DICT.keys()) + [item[::-1] for item in self.GATES_CHAKRA_DICT.keys()]
        
        full_dict["full_ch_gates_chakra_dict"] = dict(zip(full_dict["full_ch_list"], full_dict["full_ch_chakra_list"]))
        
        full_dict["full_chakra_1_list"] = [item[0] for item in full_dict["full_ch_chakra_list"]]
        full_dict["full_chakra_2_list"] = [item[1] for item in full_dict["full_ch_chakra_list"]]
        
        full_dict["full_gate_1_list"] = [item[0] for item in full_dict["full_ch_list"]]
        full_dict["full_gate_2_list"] = [item[1] for item in full_dict["full_ch_list"]]
        
        full_dict["full_gate_chakra_dict"] = dict(zip(full_dict["full_gate_1_list"], full_dict["full_chakra_1_list"]))
        
        return full_dict

def main():
 #   DOB = input("Enter your date of birth (YYYY-MM-DD): ")
 #   TOB = input("Enter your time of birth (HH:MM): ")
 #   POB = input("Enter your place of birth (City, Country): ")
    DOB = "1968-02-21"
    TOB = "11:00"
    POB = "Istanbul, Turkey"
    
    dob = datetime.strptime(DOB, "%Y-%m-%d")
    tob = datetime.strptime(TOB, "%H:%M").time()
    pob = POB
    
    chart = HumanDesignChart(dob, tob, pob)
    human_design_chart = chart.calculate_chart()
    
    print(json.dumps(human_design_chart, indent=4))

if __name__ == "__main__":
    main()
