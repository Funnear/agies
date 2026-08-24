import requests
import logging

def fetch_raw_api_sample(url, params=None, headers=None, timeout=10):
    """Generic helper to test any REST API and return raw JSON."""
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API Request Failed for URL {url}: {e}")
        return None
    except ValueError as e:
        logging.error(f"Failed to parse JSON response from {url}: {e}")
        return None