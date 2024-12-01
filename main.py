"""
Test Script for Human Design Calculations
=======================================

This script serves as a testing and demonstration module for Human Design calculations.
It performs the following operations:
1. Calculates individual Human Design features for a given birth time
2. Generates JSON output for general features, gates, and channels
3. Includes commented examples for composite calculations between two people

Key Components:
- Birth time and timezone handling
- Individual Human Design calculations
- JSON data formatting
- (Commented) Composite calculations between two people
"""

import hd_features as hd
import hd_constants
import convertJSON as cj
from geocode import get_latitude_longitude
from timezonefinder import TimezoneFinder

# Birth Time and Location Configuration
#------------------------
# Format: (year, month, day, hour, minute, second)
birth_place = 'Istanbul, Turkey'  # Birth location
birth_time = (1968,2,21,11,15,0)  # Example: February 21, 1968, 11:15 AM (DT - Design Time)
#birth_time = (1973,1,19,11,15,0)  # Alternative example (BT - Birth Time)

# Get timezone from location
#-------------------------
latitude, longitude = get_latitude_longitude(birth_place)
if latitude and longitude:
    tf = TimezoneFinder()
    zone = tf.timezone_at(lat=latitude, lng=longitude)
    if not zone:
        zone = 'Asia/Istanbul'  # Fallback timezone if lookup fails
else:
    zone = 'Asia/Istanbul'  # Fallback timezone if geocoding fails


# Timezone Calculation
#-------------------
# Get UTC offset based on timezone and birth time
# This handles historical timezone changes and daylight saving time
hours = hd.get_utc_offset_from_tz(birth_time,zone)

# Alternative: Manual timezone offset setting
#hours=8  # Example: UTC+8

# Prepare Timestamp
#----------------
# Combine birth time components with timezone offset
timestamp = tuple(list(birth_time) + [hours])

# Calculate Human Design Features
#-----------------------------
# Parameters:
# - timestamp: Birth time with timezone offset
# - report: Print detailed calculation report
# - channel_meaning: Include channel meanings
# - day_chart_only: Calculate full design (False) or day chart only (True)
single_result = hd.calc_single_hd_features(timestamp,report=True,channel_meaning=False,day_chart_only=False)

#------------------------------------------------
# JSON Output Generation
#------------------------------------------------
# Structure data for JSON conversion
# single_result array contains:
# [0] = energie_type
# [1] = inner_authority
# [2] = incarnation cross
# [4] = profile
# [5] = split definition
# [6] = gates dictionary
# [7] = active chakras
# [8] = channels
# [9] = birth date
# [10] = design crystal date
data = {
    "birth_date": single_result[9],       # Original birth time
    "create_date": single_result[10],     # Design crystal time (88° before birth)
    "energie_type": single_result[0],     # Type (Generator, Projector, etc.)
    "inner_authority": single_result[1],  # Decision-making authority
    "inc_cross": single_result[2],        # Incarnation cross
    "profile": single_result[4],          # Life role profile numbers
    "active_chakras": single_result[7],   # Defined energy centers
    "split": "{}".format(single_result[5]), # Split definition pattern
    "variables": {                        # Cognitive variables
        'right_up': 'right',     # Conscious Digestion
        'right_down': 'left',    # Conscious Environment
        'left_up': 'right',      # Unconscious Perspective
        'left_down': 'right'     # Unconscious Awareness
    }
}


# Generate and Output JSON Data
#---------------------------
# 1. General Features JSON
json_result = cj.general(data)
print(json_result)

# 2. Gates Information JSON
gatesJS = cj.gatesJSON(single_result[6]) 
print(gatesJS)

# 3. Channels Information JSON
channelsJS = cj.channelsJSON(single_result[8],False)
print(channelsJS)

#------------------------------------------------
# Composite Calculations (Currently Disabled)
#------------------------------------------------
# Example of calculating features for two people together
#hours=2 #time_zone offset for composite calculations
#define persons you want to combine
#persons_dict = {"1":(1968,2,21,11,15,0,hours), "2":(1973,1,19,11,00,0,hours)}
#print ("#composite channels and chakras")
#print (hd.get_composite_combinations(persons_dict))
#print ("#full view, with readable meanings")
#print (hd.get_composite_combinations(persons_dict).explode(["new_channels","new_ch_meaning"]))
#print ("#composite gates matching penta ")
#print (hd.get_penta(persons_dict))
