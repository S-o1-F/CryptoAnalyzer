import pytest
from api import ma_signal


# PREDICATE 1 — RACC
racc_p1_data = [
    (100, float("nan"), "HOLD"),
    (float("nan"), 100, "HOLD"),
    (100, 100, "HOLD"),
]

@pytest.mark.parametrize("price,ma,expected", racc_p1_data)
def test_ma_signal_racc_p1(price, ma, expected):
    assert ma_signal(price, ma) == expected


# PREDICATE 1 — CACC
cacc_p1_data = [
    (100, float("nan"), "HOLD"),
    (float("nan"), 100, "HOLD"),
    (100, 100, "HOLD"),
]

@pytest.mark.parametrize("price,ma,expected", cacc_p1_data)
def test_ma_signal_cacc_p1(price, ma, expected):
    assert ma_signal(price, ma) == expected


# PREDICATE 2 — RACC
racc_p2_data = [
    (110, 100, "BUY"),
    (90, 100, "SELL"),
    (100, 100, "HOLD"),
]

@pytest.mark.parametrize("price,ma,expected", racc_p2_data)
def test_ma_signal_racc_p2(price, ma, expected):
    assert ma_signal(price, ma) == expected


# PREDICATE 2 — CACC
cacc_p2_data = [
    (110, 100, "BUY"),
    (90, 100, "SELL"),
    (100, 100, "HOLD"),
]

@pytest.mark.parametrize("price,ma,expected", cacc_p2_data)
def test_ma_signal_cacc_p2(price, ma, expected):
    assert ma_signal(price, ma) == expected


# GACC
def test_ma_signal_gacc():
    # Predicate 1 - a determines result
    assert ma_signal(float("nan"), 100) == "HOLD"
    assert ma_signal(100, 100) == "HOLD"

    # Predicate 1 - b determines result
    assert ma_signal(100, float("nan")) == "HOLD"
    assert ma_signal(100, 100) == "HOLD"

    # Predicate 2 - a determines result
    assert ma_signal(110, 100) == "BUY"
    assert ma_signal(100, 100) == "HOLD"

    # Predicate 2 - b determines result
    assert ma_signal(90, 100) == "SELL"
    assert ma_signal(100, 100) == "HOLD"
