import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from fastapi import HTTPException


def test_mock_is_working():
    """Simple test to confirm mocking works"""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        import os
        result = os.path.exists("database/data.db")
        assert result == True


def test_get_symbols_returns_list():
    """Test that get_symbols() returns a list of symbols without needing the real database"""

    with patch("os.path.exists") as mock_exists, \
            patch("sqlite3.connect") as mock_connect:
        # Step 1 - fake the database file existing
        mock_exists.return_value = True

        # Step 2 - fake the database connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Step 3 - fake the cursor
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Step 4 - fake the query result
        mock_cursor.fetchall.return_value = [
            ("BTCUSDT",),
            ("ETHUSDT",),
            ("ADAUSDT",),
        ]

        # Step 5 - call the real function
        import api
        import importlib
        importlib.reload(api)

        result = api.get_symbols()

        # Step 6 - check the result
        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0]["symbol"] == "BTCUSDT"
        assert result[1]["symbol"] == "ETHUSDT"



def test_get_latest_price_returns_correct_data():
    """Test that get_latest_price() correctly returns the latest row"""

    fake_df = pd.DataFrame([
        {
            "date": "2026-01-01",
            "open": 40000.0,
            "high": 42000.0,
            "low": 39000.0,
            "close": 41000.0,
            "volume": 1500.0
        },
        {
            "date": "2026-01-02",
            "open": 41000.0,
            "high": 43000.0,
            "low": 40000.0,
            "close": 42000.0,
            "volume": 2000.0
        }
    ])

    import api
    with patch.object(api, "get_symbol_df", return_value=fake_df):
        result = api.get_latest_price("BTCUSDT")

        assert result["symbol"] == "BTCUSDT"
        assert result["close"] == 42000.0
        assert result["open"] == 41000.0
        assert result["date"] == "2026-01-02"


def test_get_symbols_database_not_found():
    """Test that get_symbols() raises an error when database does not exist"""

    with patch("os.path.exists") as mock_exists:
        # Tell it the database file does NOT exist
        mock_exists.return_value = False

        import api
        import importlib
        importlib.reload(api)

        # We expect this to raise an HTTPException
        with pytest.raises(Exception) as error:
            api.get_symbols()

        # Check the error message contains "Database not found"
        assert "Database not found" in str(error.value.detail)



def test_get_latest_price_invalid_symbol():
    """Test that get_latest_price() raises 404 when symbol does not exist"""

    # Empty DataFrame — symbol not found in database
    empty_df = pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])

    import api
    with patch.object(api, "get_symbol_df") as mock_get_df:

        # Simulate symbol not found — raise HTTPException directly
        mock_get_df.side_effect = HTTPException(
            status_code=404,
            detail="Symbol not found"
        )

        with pytest.raises(HTTPException) as error:
            api.get_latest_price("INVALIDSYMBOL999")

        # Check it returns 404
        assert error.value.status_code == 404
        assert "Symbol not found" in str(error.value.detail)


def test_get_symbols_correct_structure():
    """Test that get_symbols() correctly builds symbol structure from raw data"""

    with patch("os.path.exists") as mock_exists, \
         patch("sqlite3.connect") as mock_connect:

        mock_exists.return_value = True

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Mix of USDT and USDC symbols
        mock_cursor.fetchall.return_value = [
            ("BTCUSDT",),
            ("ETHUSDC",),
        ]

        import api
        import importlib
        importlib.reload(api)

        result = api.get_symbols()

        # Check BTCUSDT structure
        assert result[0]["symbol"] == "BTCUSDT"
        assert result[0]["base"] == "BTC"
        assert result[0]["quote"] == "USDT"

        # Check ETHUSDC structure
        assert result[1]["symbol"] == "ETHUSDC"
        assert result[1]["base"] == "ETH"
        assert result[1]["quote"] == "USDC"