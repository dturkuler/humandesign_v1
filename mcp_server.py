from flask import Flask, request, jsonify
import logging
from typing import Dict, Any, Tuple, Optional
import json

class HumanDesignMCPServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_routes(self):
        self.app.route('/calculate', methods=['GET'])(self.calculate_hd_wrapper)
    
    def validate_input_parameters(self, request_args: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[Dict[str, Any], int]]]:
        """Validate and extract input parameters from the request."""
        try:
            birth_year = int(request_args.get('year'))
            birth_month = int(request_args.get('month'))
            birth_day = int(request_args.get('day'))
            birth_hour = int(request_args.get('hour'))
            birth_minute = int(request_args.get('minute'))
            birth_second = int(request_args.get('second', 0))
            birth_place = request_args.get('place')

            if None in [birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_place]:
                return None, ({"error": "Missing required query parameters (year, month, day, hour, minute, place)"}, 400)

            birth_time = (birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second)
            return {
                'birth_time': birth_time,
                'birth_place': birth_place
            }, None

        except (TypeError, ValueError) as e:
            return None, ({"error": f"Invalid input parameter type: {e}"}, 400)
        except Exception as e:
            return None, ({"error": f"Error processing input parameters: {e}"}, 400)
    
    def process_geocoding_timezone(self, birth_time: Tuple[int, ...], birth_place: str) -> Tuple[Optional[float], Optional[float], Optional[str], Optional[Tuple[Dict[str, Any], int]]]:
        """Handle geocoding and timezone processing."""
        try:
            # These would be imported from your actual implementation
            from geocode import get_latitude_longitude
            from timezonefinder import TimezoneFinder
            import hd_features as hd
            
            latitude, longitude = get_latitude_longitude(birth_place)
            if latitude and longitude:
                tf = TimezoneFinder()
                zone = tf.timezone_at(lat=latitude, lng=longitude)
                if not zone:
                    self.logger.warning(f"Timezone lookup failed for {birth_place}. Falling back to UTC.")
                    zone = 'Etc/UTC'
            else:
                self.logger.warning(f"Geocoding failed for {birth_place}. Falling back to UTC timezone.")
                zone = 'Etc/UTC'

            hours = hd.get_utc_offset_from_tz(birth_time, zone)
            return latitude, longitude, hours, None
            
        except Exception as e:
            self.logger.error(f"Error during geocoding/timezone lookup: {e}")
            return None, None, None, ({"error": f"Error determining timezone or offset: {e}"}, 500)
    
    def calculate_hd_features(self, timestamp: Tuple[int, ...]) -> Tuple[Optional[Any], Optional[Tuple[Dict[str, Any], int]]]:
        """Calculate Human Design features."""
        try:
            import hd_features as hd
            single_result = hd.calc_single_hd_features(timestamp, report=False, channel_meaning=False, day_chart_only=False)
            return single_result, None
        except Exception as e:
            self.logger.error(f"Error during Human Design calculation: {e}")
            return None, ({"error": f"Error calculating Human Design features: {e}"}, 500)
    
    def format_output_data(self, single_result: Any) -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[Dict[str, Any], int]]]:
        """Format the output data for JSON response."""
        try:
            import convertJSON as cj
            
            data = {
                "birth_date": single_result[9],
                "create_date": single_result[10],
                "energie_type": single_result[0],
                "inner_authority": single_result[1],
                "inc_cross": single_result[2],
                "profile": single_result[4],
                "active_chakras": single_result[7],
                "split": "{}".format(single_result[5]),
                "variables": {
                    'right_up': 'right',
                    'right_down': 'left',
                    'left_up': 'right',
                    'left_down': 'right'
                }
            }

            general_json_str = cj.general(data)
            gates_json_str = cj.gatesJSON(single_result[6])
            channels_json_str = cj.channelsJSON(single_result[8], False)

            general_output = json.loads(general_json_str)
            gates_output = json.loads(gates_json_str)
            channels_output = json.loads(channels_json_str)

            final_result = {
                "general": general_output,
                "gates": gates_output,
                "channels": channels_output
            }
            
            return final_result, None
            
        except IndexError as e:
            self.logger.error(f"Error accessing calculation results: {e}. Result array: {single_result}")
            return None, ({"error": f"Error processing calculation results: Missing expected data at index {e}"}, 500)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from helper functions: {e}")
            return None, ({"error": f"Internal error generating JSON output: {e}"}, 500)
        except Exception as e:
            self.logger.error(f"Unexpected error during JSON generation: {e}")
            return None, ({"error": f"Unexpected error processing results: {e}"}, 500)
    
    def calculate_hd_wrapper(self):
        """Wrapper function to handle the entire HD calculation process."""
        # Step 1: Validate input parameters
        input_data, error_response = self.validate_input_parameters(request.args)
        if error_response:
            return jsonify(error_response[0]), error_response[1]
        
        # Step 2: Process geocoding and timezone
        _, _, hours, error_response = self.process_geocoding_timezone(
            input_data['birth_time'], input_data['birth_place']
        )
        if error_response:
            return jsonify(error_response[0]), error_response[1]
        
        # Step 3: Prepare timestamp
        timestamp = tuple(list(input_data['birth_time']) + [hours])
        
        # Step 4: Calculate HD features
        single_result, error_response = self.calculate_hd_features(timestamp)
        if error_response:
            return jsonify(error_response[0]), error_response[1]
        
        # Step 5: Format output data
        final_result, error_response = self.format_output_data(single_result)
        if error_response:
            return jsonify(error_response[0]), error_response[1]
        
        # Step 6: Return successful response
        return jsonify(final_result)
    
    def run(self, host='0.0.0.0', port=5001, debug=True):
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    server = HumanDesignMCPServer()
    server.run()