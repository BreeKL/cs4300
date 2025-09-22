"""
Module: task_requests

This module demonstrates simple helper functions using the `requests` library.
Each function is designed to be small and testable, and can be verified with
pytest and mocking (so no real network requests are required during tests).
"""

import requests


def fetch_json(url: str) -> dict:
    """
    Fetch JSON data from a given URL.

    Parameters:
    - url (str): The target URL that returns JSON.

    Returns:
    - dict: Parsed JSON response.

    Raises:
    - requests.exceptions.RequestException: If the request fails.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def url_exists(url: str) -> bool:
    """
    Check if a URL is reachable by sending a HEAD request.

    Parameters:
    - url (str): The target URL.

    Returns:
    - bool: True if status code is 200, otherwise False.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_status_code(url: str) -> int:
    """
    Return the HTTP status code from a GET request.

    Parameters:
    - url (str): The target URL.

    Returns:
    - int: The HTTP status code.
    """
    response = requests.get(url)
    return response.status_code
