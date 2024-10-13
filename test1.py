

import swisseph as swe

# Full gate mappings with zodiac degrees
GATE_MAPPINGS = {
    1: (342.0, 347.625), 2: (347.625, 353.25), 3: (353.25, 358.875), 4: (358.875, 4.5),
    5: (4.5, 10.125), 6: (10.125, 15.75), 7: (15.75, 21.375), 8: (21.375, 27.0),
    9: (27.0, 32.625), 10: (32.625, 38.25), 11: (38.25, 43.875), 12: (43.875, 49.5),
    13: (49.5, 55.125), 14: (55.125, 60.75), 15: (60.75, 66.375), 16: (66.375, 72.0),
    17: (72.0, 77.625), 18: (77.625, 83.25), 19: (83.25, 88.875), 20: (88.875, 94.5),
    21: (94.5, 100.125), 22: (100.125, 105.75), 23: (105.75, 111.375), 24: (111.375, 117.0),
    25: (117.0, 122.625), 26: (122.625, 128.25), 27: (128.25, 133.875), 28: (133.875, 139.5),
    29: (139.5, 145.125), 30: (145.125, 150.75), 31: (150.75, 156.375), 32: (156.375, 162.0),
    33: (162.0, 167.625), 34: (167.625, 173.25), 35: (173.25, 178.875), 36: (178.875, 184.5),
    37: (184.5, 190.125), 38: (190.125, 195.75), 39: (195.75, 201.375), 40: (201.375, 207.0),
    41: (207.0, 212.625), 42: (212.625, 218.25), 43: (218.25, 223.875), 44: (223.875, 229.5),
    45: (229.5, 235.125), 46: (235.125, 240.75), 47: (240.75, 246.375), 48: (246.375, 252.0),
    49: (252.0, 257.625), 50: (257.625, 263.25), 51: (263.25, 268.875), 52: (268.875, 274.5),
    53: (274.5, 280.125), 54: (280.125, 285.75), 55: (285.75, 291.375), 56: (291.375, 297.0),
    57: (297.0, 302.625), 58: (302.625, 308.25), 59: (308.25, 313.875), 60: (313.875, 319.5),
    61: (319.5, 325.125), 62: (325.125, 330.75), 63: (330.75, 336.375), 64: (336.375, 342.0)
}

# Channels connecting gates between centers
CHANNELS = {
    (1, 8): 'Channel of Inspiration (Creative Role Model)',
    (2, 14): 'Channel of the Beat (Keeper of Keys)',
    (3, 60): 'Channel of Mutation',
    (4, 63): 'Channel of Logic (Mental Ease/Doubt)',
    (5, 15): 'Channel of Rhythm',
    (6, 59): 'Channel of Intimacy (Reproduction)',
    (7, 31): 'Channel of the Alpha (Leadership)',
    (9, 52): 'Channel of Concentration (Focus)',
    (10, 20): 'Channel of Awakening (Love of Life)',
    (10, 34): 'Channel of Exploration (Discovery)',
    (12, 22): 'Channel of Openness (Social Being)',
    (13, 33): 'Channel of the Prodigal (Witness)',
    (16, 48): 'Channel of Talent (Waves of Mastery)',
    (17, 62): 'Channel of Organization (Acceptance)',
    (18, 58): 'Channel of Judgment (Correction)',
    (19, 49): 'Channel of Synthesis (Love and Needs)',
    (20, 34): 'Channel of Charisma (Power)',
    (20, 57): 'Channel of the Brainwave (Awareness)',
    (21, 45): 'Channel of Money (Materialism)',
    (23, 43): 'Channel of Structuring (Genius to Freak)',
    (24, 61): 'Channel of Awareness (Thinker)',
    (25, 51): 'Channel of Initiation (Awakener)',
    (26, 44): 'Channel of Surrender (Transmitter)',
    (27, 50): 'Channel of Preservation (Responsibility)',
    (28, 38): 'Channel of Struggle (Stubbornness)',
    (29, 46): 'Channel of Discovery (Succeeding Where Others Fail)',
    (32, 54): 'Channel of Transformation (Being Driven)',
    (35, 36): 'Channel of Transitoriness (Jack of All Trades)',
    (37, 40): 'Channel of Community (Partnership)',
    (42, 53): 'Channel of Maturation (Balanced Development)',
    (47, 64): 'Channel of Abstraction (Mental Activity/Clarity)',
    (57, 10): 'Channel of Perfected Form (Survival)',
    (57, 20): 'Channel of the Brainwave (Intuition)',
    (59, 6): 'Channel of Reproduction (Intimacy)',
    (63, 4): 'Channel of Logic (Rational Thought)'
}

# Centers and their corresponding gates
CENTER_GATE_MAP = {
    "Head": [61, 63, 64],
    "Ajna": [17, 24, 43, 47, 11],
    "Throat": [12, 16, 20, 23, 31, 33, 35, 45, 56, 62],
    "G Center": [1, 2, 7, 10, 13, 15, 25, 46],
    "Heart": [21, 26, 40, 51],
    "Sacral": [3, 9, 14, 34, 42, 53, 59],
    "Spleen": [18, 28, 32, 44, 48, 50, 57],
    "Emotional Solar Plexus": [6, 22, 30, 36, 37, 49, 55],
    "Root": [38, 39, 41, 52, 53, 58, 60]
}

# Planetary bodies used in Human Design
PLANETS = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]

# User's birth details
birth_year = 1968
birth_month = 2
birth_day = 21
birth_hour = 11
birth_minute = 0
birth_latitude = 39.9334  # Ankara, Turkey
birth_longitude = 32.8597  # Ankara, Turkey

# Step 1: Calculate planetary positions (degree) at the time of birth
julian_day = swe.julday(birth_year, birth_month, birth_day, birth_hour + birth_minute / 60)
planet_positions = {}

for planet in PLANETS:
    position, ret = swe.calc_ut(julian_day, planet)
    planet_positions[planet] = position[0]  # Store the degree

# Step 2: Map planetary positions to Human Design gates
def get_gate_from_degree(degree):
    """Map a zodiac degree to its corresponding Human Design gate."""
    degree %= 360  # Ensure the degree stays within 0-360 range
    for gate, (start, end) in GATE_MAPPINGS.items():
        if start <= degree < end:
            return gate
    return None

activated_gates = {planet: get_gate_from_degree(deg) for planet, deg in planet_positions.items()}

# Step 3: Determine defined centers
def determine_defined_centers(activated_gates):
    defined_centers = []
    for center, gates in CENTER_GATE_MAP.items():
        if any(gate in activated_gates.values() for gate in gates):
            defined_centers.append(center)
    return defined_centers

defined_centers = determine_defined_centers(activated_gates)

# Step 4: Determine energy type and strategy based on defined centers
if "Sacral" in defined_centers and "Throat" in defined_centers:
    energy_type = "Manifesting Generator"
    strategy = "To respond and then inform"
elif "Sacral" in defined_centers:
    energy_type = "Generator"
    strategy = "To respond"
elif "Throat" in defined_centers and ("Heart" in defined_centers or "G Center" in defined_centers):
    energy_type = "Manifestor"
    strategy = "To inform"
elif "Heart" in defined_centers or "G Center" in defined_centers:
    energy_type = "Projector"
    strategy = "To wait for the invitation"
else:
    energy_type = "Reflector"
    strategy = "To wait a lunar cycle"

# Step 5: Determine authority based on defined centers
def determine_authority(defined_centers):
    if "Emotional Solar Plexus" in defined_centers:
        return 'Emotional'
    elif "Sacral" in defined_centers:
        return 'Sacral'
    elif "Spleen" in defined_centers:
        return 'Splenic'
    else:
        return 'Self-Projected'

authority = determine_authority(defined_centers)

# Step 6: Determine activated channels
def determine_channels(activated_gates):
    channels = []
    for (gate1, gate2), channel in CHANNELS.items():
        if gate1 in activated_gates.values() and gate2 in activated_gates.values():
            channels.append(channel)
    return channels

activated_channels = determine_channels(activated_gates)

# Step 7: Display the calculated chart information
print(f"Energy Type: {energy_type}")
print(f"Strategy: {strategy}")
print(f"Authority: {authority}")
print(f"Activated Gates: {activated_gates}")
print(f"Defined Centers: {defined_centers}")
print(f"Activated Channels: {activated_channels}")
