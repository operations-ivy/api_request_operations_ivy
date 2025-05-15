from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from requests.exceptions import JSONDecodeError

from api_request_operations_ivy.api_request import ApiRequest


@pytest.fixture
def api():
    return ApiRequest()


def create_mock_response(status_code=200, text="{}", raise_for_status=None):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.text = text
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    else:
        mock_resp.raise_for_status.return_value = None
    return mock_resp


# --- ✅ SUCCESS TESTS --- #


@patch("api_request_operations_ivy.api_request.requests.get")
def test_get_random_success(mock_get, api):
    mock_get.return_value = create_mock_response(text='{"value": "Chuck Norris joke", "categories": []}')

    result = api.get_random()
    assert result["value"] == "Chuck Norris joke"
    assert result["categories"] == []


@patch("api_request_operations_ivy.api_request.requests.get")
def test_get_categories_success(mock_get, api):
    mock_get.return_value = create_mock_response(text='["animal", "dev", "science"]')

    result = api.get_categories()
    assert result == ["animal", "dev", "science"]


# --- ⚠️ HTTP ERROR TESTS (400 / 500) --- #


@patch("api_request_operations_ivy.api_request.requests.get")
def test_get_random_400_error(mock_get, api):
    mock_get.return_value = create_mock_response(status_code=400, raise_for_status=HTTPError("400 Client Error"))

    result = api.get_random()
    assert "HTTP error occurred" in result["error"]
    assert result["status_code"] == 400


@patch("api_request_operations_ivy.api_request.requests.get")
def test_find_specific_500_error(mock_get, api):
    mock_get.return_value = create_mock_response(status_code=500, raise_for_status=HTTPError("500 Server Error"))

    result = api.find_specific("science")
    assert "HTTP error occurred" in result["error"]
    assert result["status_code"] == 500


# --- ❌ CONNECTION & JSON ERRORS --- #


@patch("api_request_operations_ivy.api_request.requests.get")
def test_get_random_connection_error(mock_get, api):
    mock_get.side_effect = ConnectionError("Connection failed")

    result = api.get_random()
    assert "Request error" in result["error"]


@patch("api_request_operations_ivy.api_request.requests.get")
def test_get_random_json_decode_error(mock_get, api):
    mock_resp = create_mock_response(text="invalid_json")
    mock_resp.raise_for_status.return_value = None

    # Patch json.loads to raise error directly
    with patch("api_request_operations_ivy.api_request.json.loads") as mock_json_loads:
        mock_json_loads.side_effect = JSONDecodeError("Expecting value", "doc", 0)
        mock_get.return_value = mock_resp

        result = api.get_random()
        assert "Invalid JSON response" in result["error"]
