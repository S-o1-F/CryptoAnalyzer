import pytest
import sys
import os
from api import adx_signal


# TC1 - Base Choice
# C1=False, C2=>25, C3=plus_di>minus_di, C4=BUY
def test_adx_tc1_base_choice():
    result = adx_signal(30, 25, 15)
    assert result == "BUY"


# TC2 - Fixed (C4: BUY→HOLD)
# C1=True (NaN), C2=>25, C3=plus_di>minus_di, C4=HOLD
def test_adx_tc2_nan_returns_hold():
    result = adx_signal(float('nan'), 25, 15)
    assert result == "HOLD"


# TC3 - Fixed (C4: BUY→HOLD)
# C1=False, C2=<=25, C3=plus_di>minus_di, C4=HOLD
def test_adx_tc3_weak_trend_returns_hold():
    result = adx_signal(20, 25, 15)
    assert result == "HOLD"


# TC4 - Fixed (C4: BUY→HOLD)
# C1=False, C2=>25, C3=plus_di==minus_di, C4=HOLD
def test_adx_tc4_equal_di_returns_hold():
    result = adx_signal(30, 20, 20)
    assert result == "HOLD"


# TC5 - Fixed (C4: BUY→SELL)
# C1=False, C2=>25, C3=plus_di<minus_di, C4=SELL
def test_adx_tc5_bearish_returns_sell():
    result = adx_signal(30, 15, 25)
    assert result == "SELL"