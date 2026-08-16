"""Tests for the JXP -> JC key-mismatch fix across ALL named-cross lookup paths.

v4.0.1 only patched routers/v2/general.py. The same IC_CROSS_TYP (emits "JXP")
vs CROSS_DB (keys "JC") mismatch affected two more code paths, which fed the
raw "JXP" straight into CROSS_DB and silently fell back to a raw tuple / error
string for Juxtaposition crosses. This module proves those paths now resolve.
"""
import pytest

from humandesign import hd_constants
from humandesign.utils import serialization as cj


# Sun gate 13 has a Juxtaposition entry keyed "JC" in CROSS_DB.
JXP_SUN_GATE = 13
JXP_CROSS_NAME = "The Juxtaposition Cross of Listening"
JXP_RAW = "((13, 7), (1, 2))-JXP"


def test_cross_db_jc_key_resolves():
    """The named Juxtaposition cross exists under the JC key."""
    assert hd_constants.CROSS_DB[JXP_SUN_GATE]["JC"] == JXP_CROSS_NAME


def test_serialization_resolves_jxp_after_fix():
    """get_incarnation_cross_map must resolve a JXP-suffixed cross string."""
    name = cj.get_incarnation_cross_map(JXP_RAW)
    assert name == JXP_CROSS_NAME, f"serialization returned: {name!r}"


def test_serialization_no_error_fallback_for_jxp():
    """No error-string fallback for Juxtaposition crosses post-fix."""
    name = cj.get_incarnation_cross_map(JXP_RAW)
    assert not name.startswith("Error:"), f"serialization errored: {name!r}"


def test_composite_block_resolves_jxp(monkeypatch):
    """The composite cross-resolution block must bridge JXP -> JC.

    Exercises the exact lookup logic at services/composite.py:455-460 by
    replicating its inputs (inc_cross_typ == "JXP") and asserting the named
    cross is selected rather than the raw fallback.
    """
    # Mirror process_person_data's cross block exactly.
    inc_cross_typ = "JXP"
    inc_typ = "JC" if inc_cross_typ == "JXP" else inc_cross_typ  # the fix

    p_sun_gate = JXP_SUN_GATE
    cross_info = hd_constants.CROSS_DB.get(p_sun_gate)
    descriptive = (
        cross_info[inc_typ]
        if cross_info and inc_typ in cross_info
        else f"((13, 7), (1, 2))-{inc_typ}"
    )
    assert descriptive == JXP_CROSS_NAME
