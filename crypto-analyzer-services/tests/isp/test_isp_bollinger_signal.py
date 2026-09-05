from api import bollinger_signal


# TC1 - Base Choice
# C1=False, C2=inside bands, C3=True, C4=HOLD
def test_bollinger_tc1_base_choice():
    result = bollinger_signal(50, 40, 60)
    assert result == "HOLD"


# TC2 - Fixed (C4: BUY→HOLD)
# C1=True (NaN), C2=inside bands, C3=True, C4=HOLD
def test_bollinger_tc2_nan_returns_hold():
    result = bollinger_signal(float('nan'), 40, 60)
    assert result == "HOLD"


# TC3 - Fixed (C4: HOLD→BUY)
# C1=False, C2=price<lower, C3=True, C4=BUY
def test_bollinger_tc3_price_below_lower_returns_buy():
    result = bollinger_signal(30, 40, 60)
    assert result == "BUY"


# TC4 - Fixed (C4: BUY→SELL)
# C1=False, C2=price>upper, C3=True, C4=SELL
def test_bollinger_tc4_price_above_upper_returns_sell():
    result = bollinger_signal(70, 40, 60)
    assert result == "SELL"


# TC5 - Fixed (C4: BUY→HOLD)
# C1=False, C2=inside bands, C3=False, C4=HOLD
def test_bollinger_tc5_invalid_bands_returns_hold():
    result = bollinger_signal(50, 50, 50)
    assert result == "HOLD"