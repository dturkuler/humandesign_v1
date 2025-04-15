from flask import Flask, request, jsonify
import hd_features as hd
import hd_constants
import convertJSON as cj
from geocode import get_latitude_longitude
from timezonefinder import TimezoneFinder
import json # Import the json library to parse the string outputs

app = Flask(__name__)

@app.route('/calculate', methods=['GET'])
def calculate_hd():
    
    # --- 1. Get Input Parameters ---
    try:
        birth_year = int(request.args.get('year'))
        birth_month = int(request.args.get('month'))
        birth_day = int(request.args.get('day'))
        birth_hour = int(request.args.get('hour'))
        birth_minute = int(request.args.get('minute'))
        birth_second = int(request.args.get('second', 0)) # Default second to 0 if not provided
        birth_place = request.args.get('place')

        if any(v is None for v in [birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_place]):
             return jsonify({"error": "Missing required query parameters (year, month, day, hour, minute, place)"}), 400

        birth_time = (birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second)

    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input parameter type: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error processing input parameters: {e}"}), 400

    # --- 2. Geocode and Timezone ---
    try:
        latitude, longitude = get_latitude_longitude(birth_place)
        if latitude is not None and longitude is not None:
            tf = TimezoneFinder()
            zone = tf.timezone_at(lat=latitude, lng=longitude)
            # Provide a default fallback timezone if lookup fails
            if not zone:
                 print(f"Warning: Timezone lookup failed for '{birth_place}'. Falling back to UTC.")
                 zone = 'Etc/UTC' # Fallback timezone
        else:
            # Handle geocoding failure
            error_msg = f"Geocoding failed for place: '{birth_place}'. Please check the place name or try a different format."
            print(error_msg)
            return jsonify({"error": error_msg}), 400

        # --- 3. Calculate UTC Offset ---
        # Ensure birth_time is passed correctly to the offset function
        hours = hd.get_utc_offset_from_tz(birth_time, zone)

    except Exception as e:
        # Log the specific error for debugging
        print(f"Error during geocoding/timezone lookup: {e}")
        return jsonify({"error": f"Error determining timezone or offset: {e}"}), 500


    # --- 4. Prepare Timestamp ---
    timestamp = tuple(list(birth_time) + [int(hours)])
    # print(f"DEBUG: timestamp={timestamp}, zone={zone}, birth_time={birth_time}, hours={hours}", flush=True)

    # --- 5. Calculate Human Design Features ---
    try:
        # Assuming calc_single_hd_features returns the list as described in main.py
        single_result = hd.calc_single_hd_features(timestamp, report=False, channel_meaning=False, day_chart_only=False)
    except Exception as e:
        # Log the specific error for debugging
        # print(f"EXCEPTION: {e}", flush=True)
        # print(f"DEBUG: timestamp={timestamp}, zone={zone}, birth_time={birth_time}, hours={hours}", flush=True)
        return jsonify({"error": f"Error calculating Human Design features: {e}"}), 500

    # --- 6. Format Data for JSON Output ---
    # Use the same structure as main.py for consistency
    try:
        data = {
            "birth_date": single_result[9],
            "create_date": single_result[10],
            "energie_type": single_result[0],
            "inner_authority": single_result[1],
            "inc_cross": single_result[2],
            "profile": single_result[4],
            "active_chakras": single_result[7],
            "split": "{}".format(single_result[5]),
            "variables": { # Assuming static variables for now, adjust if dynamic
                'right_up': 'right',
                'right_down': 'left',
                'left_up': 'right',
                'left_down': 'right'
            }
        }

        # --- 7. Generate JSON Outputs ---
        # The convertJSON functions return JSON *strings*, we need to parse them back to objects
        general_json_str = cj.general(data)
        gates_json_str = cj.gatesJSON(single_result[6])
        channels_json_str = cj.channelsJSON(single_result[8], False)

        # Parse the JSON strings into Python dictionaries/lists
        general_output = json.loads(general_json_str)
        gates_output = json.loads(gates_json_str)
        channels_output = json.loads(channels_json_str)

    except IndexError as e:
         # Handle cases where single_result doesn't have expected indices
         print(f"Error accessing calculation results: {e}. Result array: {single_result}")
         return jsonify({"error": f"Error processing calculation results: Missing expected data at index {e}"}), 500
    except json.JSONDecodeError as e:
         # Handle errors if the convertJSON functions don't return valid JSON strings
         print(f"Error decoding JSON from helper functions: {e}")
         return jsonify({"error": f"Internal error generating JSON output: {e}"}), 500
    except Exception as e:
        # Catch any other unexpected errors during data formatting/JSON generation
        print(f"Unexpected error during JSON generation: {e}")
        return jsonify({"error": f"Unexpected error processing results: {e}"}), 500

    # --- 8. Combine and Return Results ---
    final_result = {
        "general": general_output,
        "gates": gates_output,
        "channels": channels_output
    }

    return jsonify(final_result)

if __name__ == '__main__':
    # Run the Flask app
    # Debug=True allows for auto-reloading on code changes and provides better error messages
    app.run(debug=True, port=5001) # Use a different port than default 5000 if needed
