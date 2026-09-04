import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
import requests

#za analysis service

def test_analysis_service_returns_data():
    #analysis service responds correctly

    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "symbol": "BTCUSDT",
        "rsi": 62.5,
        "macd": 150.3,
        "signal": "BUY"
    }

    import api
    with patch.object(api.requests, "get", return_value=fake_response):
        result = api.technical_analysis("BTCUSDT")

        assert result["symbol"] == "BTCUSDT"
        assert result["rsi"] == 62.5
        assert "signal" in result


def test_analysis_service_unavailable():
    #Test 503 when analysis service is not running

    import api
    with patch.object(api.requests, "get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(HTTPException) as error:
            api.technical_analysis("BTCUSDT")

        assert error.value.status_code == 503
        assert "unavailable" in error.value.detail.lower()


def test_analysis_service_timeout():
    #Test 504 when analysis service times out

    import api
    with patch.object(api.requests, "get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(HTTPException) as error:
            api.technical_analysis("BTCUSDT")

        assert error.value.status_code == 504
        assert "timed out" in error.value.detail.lower()


#za sentiment service

def test_sentiment_service_returns_data():
    #sentiment service responds correctly

    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "symbol": "BTCUSDT",
        "overall_sentiment": "positive",
        "recommendation": "BUY",
        "score": 0.75
    }

    import api
    with patch.object(api.requests, "get", return_value=fake_response):
        result = api.get_sentiment_analysis("BTCUSDT")

        assert result["symbol"] == "BTCUSDT"
        assert result["overall_sentiment"] == "positive"
        assert result["recommendation"] == "BUY"


def test_sentiment_service_unavailable():
    #test 503 when sentiment service is not running

    import api
    with patch.object(api.requests, "get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(HTTPException) as error:
            api.get_sentiment_analysis("BTCUSDT")

        assert error.value.status_code == 503
        assert "unavailable" in error.value.detail.lower()


def test_sentiment_service_timeout():
    #Test 504 when sentiment service times out

    import api
    with patch.object(api.requests, "get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(HTTPException) as error:
            api.get_sentiment_analysis("BTCUSDT")

        assert error.value.status_code == 504
        assert "timed out" in error.value.detail.lower()