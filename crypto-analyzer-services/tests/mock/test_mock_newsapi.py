import pytest
import sys
import os
from unittest.mock import patch, MagicMock

#vistinski postojt api key-to
def test_newsapi_called_when_key_exists():
    """Test that NewsAPI is called when API key is present"""

    # Fake NewsAPI response
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "status": "ok",
        "totalResults": 2,
        "articles": [
            {
                "title": "Bitcoin reaches new all time high!",
                "description": "BTC is surging with great momentum",
                "publishedAt": "2026-01-01"
            },
            {
                "title": "Crypto market looking bullish today",
                "description": "Strong growth across all major coins",
                "publishedAt": "2026-01-02"
            }
        ]
    }

    with patch("requests.get") as mock_get, \
         patch.dict(os.environ, {"NEWS_API_KEY": "fake_test_key_123"}):

        mock_get.return_value = fake_response

        import api
        import importlib
        importlib.reload(api)

        result = api.get_sentiment_analysis("BTCUSDT")

        # Check the result has the expected fields
        assert result["symbol"] == "BTCUSDT"
        assert result["base"] == "BTC"
        assert "overall_sentiment" in result
        assert "recommendation" in result
        assert result["recommendation"] in ["BUY", "SELL", "HOLD"]


def test_newsapi_skipped_when_no_key():
    """Test that NewsAPI is skipped when API key is missing"""

    with patch("requests.get") as mock_get, \
         patch.dict(os.environ, {}, clear=True):

        import api
        import importlib
        importlib.reload(api)

        result = api.get_sentiment_analysis("BTCUSDT")

        # Result should still work even without the key
        assert result["symbol"] == "BTCUSDT"
        assert "data_sources" in result
        assert "Not configured" in result["data_sources"]["news"]


def test_newsapi_handles_failure_gracefully():
    """Test that the function handles NewsAPI errors without crashing"""

    with patch("requests.get") as mock_get, \
         patch.dict(os.environ, {"NEWS_API_KEY": "fake_test_key_123"}):

        # Simulate NewsAPI timing out
        mock_get.side_effect = Exception("Connection timeout")

        import api
        import importlib
        importlib.reload(api)

        # Should not crash — should handle the error gracefully
        result = api.get_sentiment_analysis("BTCUSDT")

        assert result["symbol"] == "BTCUSDT"
        assert "overall_sentiment" in result