import pytest
from api import volume_signal


# PREDICATE 1 — RACC
racc_p1_data = [
    (float("nan"), 100, "HOLD"),
    (100, float("nan"), "HOLD"),
    (100, 100, "HOLD"),
]

@pytest.mark.parametrize("current_vol,vol_ma,expected", racc_p1_data)
def test_volume_signal_racc_p1(current_vol, vol_ma, expected):
    assert volume_signal(current_vol, vol_ma) == expected


# PREDICATE 1 — CACC
cacc_p1_data = [
    (float("nan"), 100, "HOLD"),
    (100, float("nan"), "HOLD"),
    (100, 100, "HOLD"),
]

@pytest.mark.parametrize("current_vol,vol_ma,expected", cacc_p1_data)
def test_volume_signal_cacc_p1(current_vol, vol_ma, expected):
    assert volume_signal(current_vol, vol_ma) == expected


# PREDICATE 2 — RACC
racc_p2_data = [
    (200, 100, "BUY"),
    (120, 100, "HOLD"),
    (150, 100, "HOLD"),
]

@pytest.mark.parametrize("current_vol,vol_ma,expected", racc_p2_data)
def test_volume_signal_racc_p2(current_vol, vol_ma, expected):
    assert volume_signal(current_vol, vol_ma) == expected


# PREDICATE 2 — CACC
cacc_p2_data = [
    (200, 100, "BUY"),
    (120, 100, "HOLD"),
    (150, 100, "HOLD"),
]

@pytest.mark.parametrize("current_vol,vol_ma,expected", cacc_p2_data)
def test_volume_signal_cacc_p2(current_vol, vol_ma, expected):
    assert volume_signal(current_vol, vol_ma) == expected


# GACC
def test_volume_signal_gacc():
    # Predicate 1 - a determines result
    assert volume_signal(float("nan"), 100) == "HOLD"
    assert volume_signal(100, 100) == "HOLD"

    # b determines result
    assert volume_signal(100, float("nan")) == "HOLD"
    assert volume_signal(100, 100) == "HOLD"

    # Predicate 2 - a determines result
    assert volume_signal(200, 100) == "BUY"
    assert volume_signal(100, 100) == "HOLD"

    assert volume_signal(120, 100) == "HOLD"
    assert volume_signal(150, 100) == "HOLD"