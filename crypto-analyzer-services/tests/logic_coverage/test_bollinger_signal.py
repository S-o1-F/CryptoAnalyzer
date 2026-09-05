import pytest
from api import bollinger_signal

# PREDICATE 1 — RACC
racc_p1_data = [
    (100, float("nan"), 120, "HOLD"),
    (100, 100, float("nan"), "HOLD"),
    (float("nan"), 100, 120, "HOLD"),
    (110, 100, 120, "HOLD"),
]

@pytest.mark.parametrize("price,lower,upper,expected", racc_p1_data)
def test_bollinger_signal_racc_p1(price, lower, upper, expected):
    assert bollinger_signal(price, lower, upper) == expected


# PREDICATE 1 — CACC
cacc_p1_data = [
    (100, float("nan"), 120, "HOLD"),
    (100, 100, float("nan"), "HOLD"),
    (float("nan"), 100, 120, "HOLD"),
    (110, 100, 120, "HOLD"),
]

@pytest.mark.parametrize("price,lower,upper,expected", cacc_p1_data)
def test_bollinger_signal_cacc_p1(price, lower, upper, expected):
    assert bollinger_signal(price, lower, upper) == expected


# PREDICATE 2 — RACC
racc_p2_data = [
    (90, 100, 120, "BUY"),
    (130, 100, 120, "SELL"),
    (110, 100, 120, "HOLD"),
]

@pytest.mark.parametrize("price,lower,upper,expected", racc_p2_data)
def test_bollinger_signal_racc_p2(price, lower, upper, expected):
    assert bollinger_signal(price, lower, upper) == expected


# PREDICATE 2 — CACC
cacc_p2_data = [
    (90, 100, 120, "BUY"),
    (130, 100, 120, "SELL"),
    (110, 100, 120, "HOLD"),
]

@pytest.mark.parametrize("price,lower,upper,expected", cacc_p2_data)
def test_bollinger_signal_cacc_p2(price, lower, upper, expected):
    assert bollinger_signal(price, lower, upper) == expected


# GACC
def test_bollinger_signal_gacc():
    # Predicate 1 - a determines result
    assert bollinger_signal(100, float("nan"), 120) == "HOLD"
    assert bollinger_signal(110, 100, 120) == "HOLD"

    # Predicate 1 - b determines result
    assert bollinger_signal(100, 100, float("nan")) == "HOLD"
    assert bollinger_signal(110, 100, 120) == "HOLD"

    # Predicate 1 - c determines result
    assert bollinger_signal(float("nan"), 100, 120) == "HOLD"
    assert bollinger_signal(110, 100, 120) == "HOLD"

    # Predicate 2 - d determines result
    assert bollinger_signal(90, 100, 120) == "BUY"
    assert bollinger_signal(110, 100, 120) == "HOLD"

    # Predicate 2 - e determines result
    assert bollinger_signal(130, 100, 120) == "SELL"
    assert bollinger_signal(110, 100, 120) == "HOLD"
