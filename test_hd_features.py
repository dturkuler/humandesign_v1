import pytest
from datetime import datetime
import pytz
import numpy as np
from hd_features import (
    get_utc_offset_from_tz,
    hd_features,
    get_inc_cross,
    get_profile,
    get_variables,
    is_connected,
    get_auth,
    get_typ,
    get_component,
    get_channels_and_active_chakras,
    get_split,
    calc_single_hd_features,
    unpack_single_features
)
import hd_constants

# Test data - Known Human Design chart for testing
# This is a Generator type chart
TEST_TIMESTAMP = (1990, 3, 15, 14, 30, 0, 1)  # A known Generator chart
TEST_TIMEZONE = "Europe/Berlin"

def test_get_utc_offset_from_tz():
    """Test UTC offset calculation for different timezones and dates"""
    # Test winter time
    winter_timestamp = (2023, 1, 1, 12, 0, 0)
    offset = get_utc_offset_from_tz(winter_timestamp, "Europe/Berlin")
    assert offset == 1.0  # Berlin is UTC+1 in winter

    # Test summer time (DST)
    summer_timestamp = (2023, 7, 1, 12, 0, 0)
    offset = get_utc_offset_from_tz(summer_timestamp, "Europe/Berlin")
    assert offset == 2.0  # Berlin is UTC+2 in summer

    # Test timezone with different offset
    tokyo_offset = get_utc_offset_from_tz(winter_timestamp, "Asia/Tokyo")
    assert tokyo_offset == 9.0  # Tokyo is UTC+9

def test_hd_features_initialization():
    """Test initialization of HD Features class"""
    hd = hd_features(*TEST_TIMESTAMP)
    
    # Check if attributes are set correctly
    assert hd.year == TEST_TIMESTAMP[0]
    assert hd.month == TEST_TIMESTAMP[1]
    assert hd.day == TEST_TIMESTAMP[2]
    assert hd.hour == TEST_TIMESTAMP[3]
    assert hd.minute == TEST_TIMESTAMP[4]
    assert hd.second == TEST_TIMESTAMP[5]
    assert hd.tz_offset == TEST_TIMESTAMP[6]
    
    # Check if constants are loaded
    assert hasattr(hd, 'SWE_PLANET_DICT')
    assert hasattr(hd, 'IGING_CIRCLE_LIST')
    assert hasattr(hd, 'CHAKRA_LIST')

def test_timestamp_to_juldate():
    """Test conversion of timestamp to Julian date"""
    hd = hd_features(*TEST_TIMESTAMP)
    jul_date = hd.timestamp_to_juldate()
    
    # Julian date should be within a reasonable range
    assert isinstance(jul_date, float)
    assert 2440000.0 <= jul_date <= 2460000.0  # Valid range for recent dates

def test_calc_single_hd_features():
    """Test calculation of single HD features"""
    # Return values: typ, auth, inc_cross, inc_cross_typ, profile, split, date_to_gate_dict, active_chakras, active_channels_dict, bdate, cdate
    result = calc_single_hd_features(TEST_TIMESTAMP)
    
    # Print test results
    print("\n=== Human Design Features Test Results ===")
    typ, auth, inc_cross, inc_cross_typ, profile, split, date_to_gate_dict, active_chakras, active_channels_dict, bdate, cdate = result
    print(f"Type: {typ}")
    print(f"Authority: {auth}")
    print(f"Incarnation Cross: {inc_cross}")
    print(f"Cross Type: {inc_cross_typ}")
    print(f"Profile: {profile}")
    print(f"Split: {split}")
    print(f"Active Chakras: {sorted(list(active_chakras))}")
    print("\nActive Channels:")
    for channel, details in active_channels_dict.items():
        print(f"  {channel}: {details}")
    print(f"\nBirth Date: {bdate}")
    print(f"Calculation Date: {cdate}")
    print("=" * 40 + "\n")
    
    # Check the structure of the result
    assert isinstance(result, tuple)
    assert len(result) == 11  # Should have 11 elements
    
    # Unpack values
    typ, auth, inc_cross, inc_cross_typ, profile, split, date_to_gate_dict, active_chakras, active_channels_dict, bdate, cdate = result
    
    # Test individual components
    assert isinstance(typ, str)
    assert isinstance(auth, str)
    assert isinstance(inc_cross, str)  # inc_cross is returned as a string in format "((x,y),(z,w))-TYPE"
    assert "-" in inc_cross  # Should contain the cross type
    assert isinstance(profile, tuple)
    assert isinstance(split, (int, np.integer))  # Allow both Python int and NumPy integer types
    assert isinstance(date_to_gate_dict, dict)
    assert isinstance(active_chakras, set)
    assert isinstance(active_channels_dict, dict)
    assert isinstance(bdate, str)
    assert isinstance(cdate, str)

def test_get_channels_and_active_chakras():
    """Test channel and chakra activation calculation"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    date_to_gate_dict = result[6]  # Index 6 is date_to_gate_dict
    
    channels, chakras = get_channels_and_active_chakras(date_to_gate_dict)
    
    # Check channels
    assert isinstance(channels, dict)
    assert "label" in channels
    assert "planets" in channels
    assert "gate" in channels
    assert "ch_gate" in channels
    
    # Check chakras
    assert isinstance(chakras, set)
    assert all(chakra in hd_constants.CHAKRA_LIST for chakra in chakras)

def test_get_auth():
    """Test authority determination"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    active_channels = result[8]  # Index 8 is active_channels_dict
    active_chakras = result[7]   # Index 7 is active_chakras
    
    auth = get_auth(active_chakras, active_channels)
    assert auth in {"SP", "SL", "SN", "HT", "GC", "HT_GC", "outer"}

def test_get_typ():
    """Test Human Design type determination"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    active_channels = result[8]  # Index 8 is active_channels_dict
    active_chakras = result[7]   # Index 7 is active_chakras
    
    typ = get_typ(active_channels, active_chakras)
    assert typ in {"GENERATOR", "MANIFESTING GENERATOR", "PROJECTOR", "MANIFESTOR", "REFLECTOR"}

def test_get_profile():
    """Test profile calculation"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    date_to_gate_dict = result[6]  # Index 6 is date_to_gate_dict
    
    profile = get_profile(date_to_gate_dict)
    assert isinstance(profile, tuple)
    assert len(profile) == 2
    assert all(1 <= x <= 6 for x in profile)

def test_get_variables():
    """Test variables calculation"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    date_to_gate_dict = result[6]  # Index 6 is date_to_gate_dict
    
    variables = get_variables(date_to_gate_dict)
    assert isinstance(variables, dict)
    assert all(key in variables for key in ["right_up", "right_down", "left_up", "left_down"])

def test_get_split():
    """Test split determination"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    active_channels = result[8]  # Index 8 is active_channels_dict
    active_chakras = result[7]   # Index 7 is active_chakras
    
    split = get_split(active_channels, active_chakras)
    assert isinstance(split, (int, np.integer))  # Allow both Python int and NumPy integer types
    assert split in {-1, 0, 1, 2, 3, 4}

def test_is_connected():
    """Test chakra connection checking"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    active_channels = result[8]  # Index 8 is active_channels_dict
    
    # Test some common connections
    assert isinstance(is_connected(active_channels, "TT", "AA"), bool)
    assert isinstance(is_connected(active_channels, "HD", "RT"), bool)
    assert isinstance(is_connected(active_channels, "TT", "SN", "RT"), bool)

def test_get_component():
    """Test component determination for chakras"""
    result = calc_single_hd_features(TEST_TIMESTAMP)
    active_channels = result[8]  # Index 8 is active_channels_dict
    
    # Test for each chakra
    for chakra in hd_constants.CHAKRA_LIST:
        component = get_component(active_channels, chakra)
        assert isinstance(component, (str, type(None)))
        if component:
            gates = component.split("-")
            assert all(gate.isdigit() for gate in gates)
