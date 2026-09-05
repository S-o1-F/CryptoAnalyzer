from api import ma_signal


# TC1 - Base Choice
# C1=False, C2=price>ma, C3=price>0, C4=BUY
def test_ma_tc1_base_choice():
    result = ma_signal(55, 50)
    assert result == "BUY"


# TC2 - Fixed (C4: BUY→HOLD)
# C1=True (NaN), C2=price>ma, C3=price>0, C4=HOLD
def test_ma_tc2_nan_returns_hold():
    result = ma_signal(float('nan'), 50)
    assert result == "HOLD"


# TC3 - Fixed (C4: BUY→HOLD)
# C1=False, C2=price==ma, C3=price>0, C4=HOLD
def test_ma_tc3_equal_price_returns_hold():
    result = ma_signal(50, 50)
    assert result == "HOLD"


# TC4 - Fixed (C4: BUY→SELL)
# C1=False, C2=price<ma, C3=price>0, C4=SELL
def test_ma_tc4_price_below_ma_returns_sell():
    result = ma_signal(45, 50)
    assert result == "SELL"


# TC5 - Feasible
# C1=False, C2=price>ma, C3=price==0, C4=BUY
def test_ma_tc5_zero_price_returns_buy():
    result = ma_signal(0, -5)
    assert result == "BUY"


# TC6 - Feasible
# C1=False, C2=price>ma, C3=price<0, C4=BUY
def test_ma_tc6_negative_price_returns_buy():
    result = ma_signal(-5, -10)
    assert result == "BUY"