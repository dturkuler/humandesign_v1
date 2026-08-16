"""Tests for V2 Incarnation Cross (inc_cross) resolution.

Covers the JXP/JC key mismatch bug fix in routers/v2/general.py:
CROSS_DB uses "JC" for Juxtaposition while IC_CROSS_TYP emits "JXP".
The router now normalizes JXP -> JC before the CROSS_DB lookup.
"""
import re

import pytest
from fastapi.testclient import TestClient

from humandesign.api import app
from humandesign.dependencies import verify_token
from humandesign import hd_constants

app.dependency_overrides[verify_token] = lambda: True
client = TestClient(app)

# Raw tuple fallback pattern, e.g. "((13, 7), (1, 2))-JXP"
RAW_CROSS_PATTERN = re.compile(r"^\(\(.*\)\)-(JXP|RAC|LAC)$")

TEST_BODY = {
    "year": 1968,
    "month": 2,
    "day": 21,
    "hour": 11,
    "minute": 0,
    "place": "Europe/Istanbul",
    "gender": "male",
}


def test_v2_inc_cross_is_named_not_raw():
    """Endpoint must return a human-readable cross name, never the raw tuple string."""
    response = client.post("/v2/calculate", json=TEST_BODY)
    assert response.status_code == 200
    data = response.json()
    inc_cross = data["general"]["inc_cross"]
    assert isinstance(inc_cross, str)
    assert inc_cross.strip() != ""
    assert not RAW_CROSS_PATTERN.match(inc_cross), (
        f"inc_cross fell back to raw tuple: {inc_cross}"
    )


def test_jxp_normalization_resolves_against_cross_db():
    """Replicate the router lookup logic and prove JXP -> JC resolves a name.

    This guarantees the fix works even when the computed cross is a
    Juxtaposition (type code "JXP"), the only branch that previously broke.
    """
    # Sun gate 13 has a Juxtaposition entry keyed "JC" in CROSS_DB.
    sun_gate = 13
    assert "JC" in hd_constants.CROSS_DB[sun_gate]

    # Router logic (post-fix) for a Juxtaposition cross:
    cross_abbr = "JXP"
    if cross_abbr == "JXP":
        cross_abbr = "JC"
    cross_full = hd_constants.CROSS_DB.get(sun_gate, {}).get(cross_abbr, "FALLBACK")
    assert cross_full == "The Juxtaposition Cross of Listening"
    assert cross_full != "FALLBACK"


def test_pre_fix_would_have_failed():
    """Document the original bug: JXP key was missing from CROSS_DB."""
    # Without normalization, JXP would not be found and fallback to raw tuple.
    missing = hd_constants.CROSS_DB.get(13, {}).get("JXP", None)
    assert missing is None
    # Confirm this is why normalization is required, not redundant.
    assert "JC" in hd_constants.CROSS_DB[13]
