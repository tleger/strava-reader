from unittest.mock import patch, Mock
from typing import Optional

import pytest
import httpx

from modules.strava_api import get_access_token, fetch_activities

# Helper function to create a mock response
def create_mock_response(
    json_data: dict | list, raise_for_status: Optional[Mock] = None
) -> Mock:
    mock_response = Mock()
    mock_response.json.return_value = json_data
    mock_response.raise_for_status = raise_for_status or Mock()
    return mock_response


# Test get_access_token function
@patch("httpx.post")
def test_get_access_token_success(mock_post: Mock):
    """Test get_access_token successfully retrieves an access token."""
    mock_post.return_value = create_mock_response({"access_token": "mock_access_token"})
    access_token = get_access_token()
    assert access_token == "mock_access_token"


@patch("httpx.post")
def test_get_access_token_failure(mock_post: Mock):
    """Test get_access_token handles HTTPStatusError."""
    mock_post.side_effect = httpx.HTTPStatusError(
        "Mocked error", request=Mock(), response=Mock()
    )

    with pytest.raises(httpx.HTTPStatusError):
        get_access_token()


# Test fetch_activities function
@patch("httpx.get")
def test_fetch_activities_success(mock_get: Mock):
    """Test fetch_activities successfully retrieves activities."""
    mock_get.return_value = create_mock_response([{"id": 1, "name": "Test Activity"}])

    activities = fetch_activities("mock_access_token")

    assert len(activities) == 1
    assert activities[0]["id"] == 1
    assert activities[0]["name"] == "Test Activity"


@patch("httpx.get")
def test_fetch_activities_no_data(mock_get: Mock):
    """Test fetch_activities handles no data scenario."""
    mock_get.return_value = create_mock_response([])
    activities = fetch_activities("mock_access_token")
    assert len(activities) == 0


@patch("httpx.get")
def test_fetch_activities_request_error(mock_get: Mock):
    """Test fetch_activities handles RequestError."""
    mock_get.side_effect = httpx.RequestError("Mocked error", request=Mock())

    activities = fetch_activities("mock_access_token")

    assert len(activities) == 0


@patch("httpx.get")
def test_fetch_activities_http_error(mock_get: Mock):
    """Test fetch_activities handles HTTPStatusError."""
    mock_get.side_effect = httpx.HTTPStatusError(
        "Mocked error", request=Mock(), response=Mock()
    )

    activities = fetch_activities("mock_access_token")

    assert len(activities) == 0
