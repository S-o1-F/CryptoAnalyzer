import pytest
from api import rsi_signal   # adjust import path if needed

# PREDICATE 1 — RACC
racc_p1_data = [
    (float("nan"), "HOLD"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("rsi,expected", racc_p1_data)
def test_rsi_signal_racc_p1(rsi, expected):
    assert rsi_signal(rsi) == expected


# PREDICATE 1 — CACC
cacc_p1_data = [
    (float("nan"), "HOLD"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("rsi,expected", cacc_p1_data)
def test_rsi_signal_cacc_p1(rsi, expected):
    assert rsi_signal(rsi) == expected


# PREDICATE 2 — RACC
racc_p2_data = [
    (25, "BUY"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("rsi,expected", racc_p2_data)
def test_rsi_signal_racc_p2(rsi, expected):
    assert rsi_signal(rsi) == expected


# PREDICATE 2 — CACC
cacc_p2_data = [
    (25, "BUY"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("rsi,expected", cacc_p2_data)
def test_rsi_signal_cacc_p2(rsi, expected):
    assert rsi_signal(rsi) == expected


# PREDICATE 3 — RACC]
racc_p3_data = [
    (75, "SELL"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("rsi,expected", racc_p3_data)
def test_rsi_signal_racc_p3(rsi, expected):
    assert rsi_signal(rsi) == expected


# PREDICATE 3 — CACC
cacc_p3_data = [
    (75, "SELL"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("rsi,expected", cacc_p3_data)
def test_rsi_signal_cacc_p3(rsi, expected):
    assert rsi_signal(rsi) == expected


# GACC
def test_rsi_signal_gacc():
    # Predicate 1 - a determines result
    assert rsi_signal(float("nan")) == "HOLD"
    assert rsi_signal(50) == "HOLD"

    # Predicate 2 - a determines result (rsi < 30)
    assert rsi_signal(25) == "BUY"
    assert rsi_signal(50) == "HOLD"

    # boundary <30
    assert rsi_signal(29.9) == "BUY"
    assert rsi_signal(30) == "HOLD"

    # Predicate 3 - a determines result (rsi > 70)
    assert rsi_signal(75) == "SELL"
    assert rsi_signal(50) == "HOLD"

    # boundary >70
    assert rsi_signal(70.1) == "SELL"
    assert rsi_signal(70) == "HOLD"