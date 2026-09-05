import pytest
from api import stochastic_signal


# PREDICATE 1 — RACC
racc_p1_data = [
    (float("nan"), "HOLD"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("stoch,expected", racc_p1_data)
def test_stochastic_signal_racc_p1(stoch, expected):
    assert stochastic_signal(stoch) == expected


# PREDICATE 1 — CACC
cacc_p1_data = [
    (float("nan"), "HOLD"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("stoch,expected", cacc_p1_data)
def test_stochastic_signal_cacc_p1(stoch, expected):
    assert stochastic_signal(stoch) == expected


# PREDICATE 2 — RACC
racc_p2_data = [
    (15, "BUY"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("stoch,expected", racc_p2_data)
def test_stochastic_signal_racc_p2(stoch, expected):
    assert stochastic_signal(stoch) == expected


# PREDICATE 2 — CACC
cacc_p2_data = [
    (15, "BUY"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("stoch,expected", cacc_p2_data)
def test_stochastic_signal_cacc_p2(stoch, expected):
    assert stochastic_signal(stoch) == expected


# PREDICATE 3 — RACC
racc_p3_data = [
    (85, "SELL"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("stoch,expected", racc_p3_data)
def test_stochastic_signal_racc_p3(stoch, expected):
    assert stochastic_signal(stoch) == expected


# PREDICATE 3 — CACC
cacc_p3_data = [
    (85, "SELL"),
    (50, "HOLD"),
]

@pytest.mark.parametrize("stoch,expected", cacc_p3_data)
def test_stochastic_signal_cacc_p3(stoch, expected):
    assert stochastic_signal(stoch) == expected


# GACC
def test_stochastic_signal_gacc():
    # Predicate 1 - a determines result
    assert stochastic_signal(float("nan")) == "HOLD"
    assert stochastic_signal(50) == "HOLD"

    # Predicate 2 - a determines result (stoch < 20)
    assert stochastic_signal(15) == "BUY"
    assert stochastic_signal(50) == "HOLD"

    # boundary <20
    assert stochastic_signal(19.9) == "BUY"
    assert stochastic_signal(20) == "HOLD"

    # Predicate 3 - a determines result
    assert stochastic_signal(85) == "SELL"
    assert stochastic_signal(50) == "HOLD"

    # boundary >80
    assert stochastic_signal(80.1) == "SELL"
    assert stochastic_signal(80) == "HOLD"