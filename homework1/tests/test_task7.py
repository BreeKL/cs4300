import pytest
import requests
from unittest.mock import patch, MagicMock
from task7 import fetch_json, url_exists, get_status_code


@patch("task7.requests.get")
def test_fetch_json(mock_get):
    # Mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_json("https://example.com/api/user")
    assert result == {"id": 1, "name": "Alice"}
    mock_get.assert_called_once_with("https://example.com/api/user")


@patch("task7.requests.head")
def test_url_exists_true(mock_head):
    mock_response = MagicMock(status_code=200)
    mock_head.return_value = mock_response

    assert url_exists("https://example.com") is True
    mock_head.assert_called_once()


def test_google_url():
    assert url_exists("https://www.google.com") is True


@patch("task7.requests.head")
def test_url_exists_false(mock_head):
    mock_response = MagicMock(status_code=404)
    mock_head.return_value = mock_response

    assert url_exists("https://example.com") is False


@patch("task7.requests.head")
def test_url_exists_exception(mock_head):
    mock_head.side_effect = requests.RequestException("Network error")
    assert url_exists("https://bad-url.com") is False


@patch("task7.requests.get")
def test_get_status_code(mock_get):
    mock_response = MagicMock(status_code=404)
    mock_get.return_value = mock_response

    code = get_status_code("https://example.com/missing")
    assert code == 404
    mock_get.assert_called_once()
