import pytest
from api import adx_signal


# PREDICATE 1 — RACC
racc_p1_data = [
    (float('nan'), 25, 15, "HOLD"),
    (30, float('nan'), 15, "HOLD"),
    (30, 25, float('nan'), "HOLD"),
    (30, 25, 15, "BUY"),
]

@pytest.mark.parametrize("adx,plus_di,minus_di,expected", racc_p1_data)
def test_adx_signal_racc_p1(adx, plus_di, minus_di, expected):
    assert adx_signal(adx, plus_di, minus_di) == expected


# PREDICATE 1 — CACC
cacc_p1_data = [
    (float('nan'), 25, 15, "HOLD"),
    (30, float('nan'), 15, "HOLD"),
    (30, 25, float('nan'), "HOLD"),
    (30, 25, 15, "BUY"),
]

@pytest.mark.parametrize("adx,plus_di,minus_di,expected", cacc_p1_data)
def test_adx_signal_cacc_p1(adx, plus_di, minus_di, expected):
    assert adx_signal(adx, plus_di, minus_di) == expected


# PREDICATE 2 — RACC
racc_p2_data = [
    (30, 25, 15, "BUY"),
    (30, 15, 25, "SELL"),
    (30, 20, 20, "HOLD"),
    (20, 25, 15, "HOLD"),
]

@pytest.mark.parametrize("adx,plus_di,minus_di,expected", racc_p2_data)
def test_adx_signal_racc_p2(adx, plus_di, minus_di, expected):
    assert adx_signal(adx, plus_di, minus_di) == expected


# PREDICATE 2 — CACC
cacc_p2_data = [
    (30, 25, 15, "BUY"),
    (30, 15, 25, "SELL"),
    (30, 20, 20, "HOLD"),
    (20, 25, 15, "HOLD"),
]

@pytest.mark.parametrize("adx,plus_di,minus_di,expected", cacc_p2_data)
def test_adx_signal_cacc_p2(adx, plus_di, minus_di, expected):
    assert adx_signal(adx, plus_di, minus_di) == expected

# GACC
def test_adx_signal_gacc():
    # Predicate 1 - a determines result
    assert adx_signal(float('nan'), 25, 15) == "HOLD"
    assert adx_signal(30, 25, 15) == "BUY"

    # Predicate 1 - b determines result
    assert adx_signal(30, float('nan'), 15) == "HOLD"
    assert adx_signal(30, 25, 15) == "BUY"

    # Predicate 1 - c determines result
    assert adx_signal(30, 25, float('nan')) == "HOLD"
    assert adx_signal(30, 25, 15) == "BUY"

    # Predicate 2 - d determines result
    assert adx_signal(30, 25, 15) == "BUY"
    assert adx_signal(20, 25, 15) == "HOLD"

    # Predicate 2 - e determines result
    assert adx_signal(30, 25, 15) == "BUY"
    assert adx_signal(30, 20, 20) == "HOLD"

    # Predicate 2 - f determines result
    assert adx_signal(30, 15, 25) == "SELL"
    assert adx_signal(30, 20, 20) == "HOLD"