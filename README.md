# Human Design Project

## Overview
This project is a collection of Python scripts and modules that provide functionalities related to Human Design, a system of knowledge that combines astrology, kabbalah, and the I Ching to map the energy flows within a person. The project includes functionalities for geocoding, calculating Human Design features, and providing an API for these calculations.

## Project Structure

- **api_.py**: Flask API for calculating Human Design features.
- **convertJSON.py**: Functions to convert data into JSON format.
- **geocode.py**: Functions for geocoding and calculating distances.
- **hd_constants.py**: Constants used in Human Design calculations.
- **hd_features.py**: Classes and functions for calculating Human Design features.
- **mcp_server.py**: MCP server for processing Human Design calculations.

## File Descriptions

### api_.py
This file contains the Flask API for calculating Human Design features.

#### Functions
- **calculate_hd()**: Calculates Human Design features based on the provided input.

### convertJSON.py
This file contains functions to convert data into JSON format.

#### Functions
- **general(data)**: Converts general data into JSON format.
- **gatesJSON(data, details=False)**: Converts gate data into JSON format.
- **channelsJSON(data, details=False)**: Converts channel data into JSON format.

### geocode.py
This file contains functions for geocoding and calculating distances.

#### Classes
- **Location**: Data class for storing location information.

#### Functions
- **get_latitude_longitude(place: str) -> Tuple[Optional[float], Optional[float]]**: Retrieves latitude and longitude for a given place.
- **get_address(latitude: float, longitude: float) -> Optional[str]**: Retrieves address for given latitude and longitude.
- **batch_geocode(places: List[str]) -> List[Location]**: Geocodes a list of places.
- **calculate_distance(place1: str, place2: str) -> Optional[float]**: Calculates the distance between two places.

### hd_constants.py
This file contains constants used in Human Design calculations.

#### Constants
- **SWE_PLANET_DICT**: Dictionary of planets and their corresponding indices.
- **GATES_CHAKRA_DICT**: Dictionary of gates and their corresponding chakras.
- **CHANNEL_MEANING_DICT**: Dictionary of channel meanings.
- **IC_CROSS_TYP**: Dictionary of IC cross types.
- **penta_dict**: Dictionary of penta types.
- **circuit_typ_dict**: Dictionary of circuit types.
- **circuit_group_typ_dict**: Dictionary of circuit group types.
- **awareness_stream_dict**: Dictionary of awareness stream types.
- **awareness_stream_group_dict**: Dictionary of awareness stream group types.

### hd_features.py
This file contains classes and functions for calculating Human Design features.

#### Classes
- **hd_features**: Class for calculating Human Design features.
- **hd_composite**: Class for calculating composite Human Design features.

#### Functions
- **get_utc_offset_from_tz(timestamp, zone)**: Retrieves UTC offset for a given timezone.
- **timestamp_to_juldate(self, *time_stamp)**: Converts timestamp to Julian date.
- **calc_create_date(self, jdut)**: Calculates creation date from Julian date.
- **date_to_gate(self, jdut, label)**: Converts date to gate.
- **birth_creat_date_to_gate(self, *time_stamp)**: Converts birth creation date to gate.
- **day_chart(self, *time_stamp)**: Generates day chart.
- **get_inc_cross(date_to_gate_dict)**: Retrieves incidence cross.
- **get_profile(date_to_gate_dict)**: Retrieves profile.
- **get_variables(date_to_gate_dict)**: Retrieves variables.
- **is_connected(active_channels_dict, *args)**: Checks if channels are connected.
- **get_auth(active_chakras, active_channels_dict)**: Retrieves authentication.
- **get_typ_old(active_channels_dict, active_chakras)**: Retrieves type (old method).
- **get_typ(active_channels_dict, active_chakras)**: Retrieves type.
- **get_component(active_channels_dict, chakra)**: Retrieves component.
- **get_channels_and_active_chakras(date_to_gate_dict, meaning=False)**: Retrieves channels and active chakras.
- **get_split(active_channels_dict, active_chakras)**: Retrieves split.
- **calc_full_gates_chakra_dict(gates_chakra_dict)**: Calculates full gates chakra dictionary.
- **calc_full_channel_meaning_dict()**: Calculates full channel meaning dictionary.
- **chakra_connection_list(chakra_1, chakra_2)**: Retrieves chakra connection list.
- **get_full_chakra_connect_dict()**: Retrieves full chakra connection dictionary.
- **calc_single_hd_features(timestamp, report=False, channel_meaning=False, day_chart_only=False)**: Calculates single Human Design features.
- **unpack_single_features(single_result)**: Unpacks single features.
- **get_timestamp_list(start_date, end_date, percentage, time_unit, intervall)**: Retrieves timestamp list.
- **calc_mult_hd_features(start_date, end_date, percentage, time_unit, intervall, num_cpu)**: Calculates multiple Human Design features.
- **unpack_mult_features(result, full=True)**: Unpacks multiple features.
- **get_single_hd_features(persons_dict, key, feature)**: Retrieves single Human Design features.
- **composite_chakras_channels(persons_dict, identity, other_person)**: Retrieves composite chakras and channels.
- **get_composite_combinations(persons_dict)**: Retrieves composite combinations.
- **get_penta(persons_dict, report=False)**: Retrieves penta.

### mcp_server.py
This file contains the MCP server for processing Human Design calculations.

#### Classes
- **HumanDesignMCPServer**: Class for the MCP server.

#### Functions
- **setup_logging(self)**: Sets up logging.
- **validate_input_parameters(self, request_args: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[Dict[str, Any], int]]]**: Validates input parameters.
- **process_geocoding_timezone(self, birth_time: Tuple[int, ...], birth_place: str) -> Tuple[Optional[float], Optional[float], Optional[str], Optional[Tuple[Dict[str, Any], int]]]**: Processes geocoding and timezone.
- **calculate_hd_features(self, timestamp: Tuple[int, ...]) -> Tuple[Optional[Any], Optional[Tuple[Dict[str, Any], int]]]**: Calculates Human Design features.
- **format_output_data(self, single_result: Any) -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[Dict[str, Any], int]]]**: Formats output data.
- **calculate_hd_wrapper(self)**: Wrapper for calculating Human Design features.

## Usage
To use the project, you can run the Flask API in `api_.py` and make requests to the `/calculate` endpoint. The MCP server in `mcp_server.py` can be used to process Human Design calculations.

## Requirements
- Python 3.8 or higher
- Flask
- Geopy
- NumPy

## Installation
1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the Flask API using `python api_.py`.
4. Run the MCP server using `python mcp_server.py`.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.