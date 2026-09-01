import logging

import pandas as pd
import requests

# Initialize dedicated module logger (Fixes LOG015)
logger = logging.getLogger(__name__)


def fetch_raw_api_sample(
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    timeout: int = 10,
) -> dict | list | None:
    """Generic helper to test any REST API and return raw JSON."""
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API Request Failed for URL {url}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON response from {url}: {e}")
        return None


def transform_sparql_bindings_to_dataframe(raw_response: dict) -> pd.DataFrame:
    """
    Extracts raw SPARQL JSON bindings into a flat Pandas DataFrame.
    Dynamically maps every variable key returned in the SPARQL results.
    """
    try:
        if not raw_response or "results" not in raw_response:
            logger.warning("Response payload is empty or invalid SPARQL JSON.")
            return pd.DataFrame()

        bindings = raw_response.get("results", {}).get("bindings", [])

        parsed_rows = []
        for item in bindings:
            row = {var_name: data.get("value") for var_name, data in item.items()}
            parsed_rows.append(row)

        return pd.DataFrame(parsed_rows)

    except (KeyError, TypeError, AttributeError) as e:
        # Catch specific transformation errors (Fixes BLE001)
        logger.error(f"Failed to transform SPARQL bindings to DataFrame: {e}")
        return pd.DataFrame()
