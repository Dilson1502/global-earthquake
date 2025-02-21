import requests  # type: ignore
import geopy.distance  # type: ignore
import os

from typing import Any, Dict, Union, List, Tuple
from dotenv import load_dotenv

from src.transformations.check_dotenv import check_dotenv_presence

# Load environment variable from .env file if present.
load_dotenv()

# Check dotenv
check_dotenv_presence()

# Get API URL
API_URL = os.getenv("API_URL")


def api_response() -> Union[List[Dict[str, Any]], None]:
    """Call earthquakes API.

    Returns:
        Union[List[Dict[str, Any]], None]: JSON with all earthquaked metadata or None if no response.
    """
    try:
        response = requests.get(API_URL, verify=False, timeout=10) # Added timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json().get("features")
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None


def filter_api_response(earthquake_list: List[Dict[str, Any]]) -> Dict[str, Dict[str, Tuple[float, float]]]:
    """Filter API response, obtain only earthquakes titles and location.

    Args:
        earthquake_list (List[Dict[str, Any]]): list of earthquakes from API response.

    Returns:
        earthquake_dict (Dict[str, Dict[str, Tuple[float, float]]]): a dict containing filtered data of id,
        title and coordinates.
    """
    earthquake_dict = {}

    for earthquake in earthquake_list:
        earthquake_id = earthquake.get("id")
        properties = earthquake.get("properties")
        geometry = earthquake.get("geometry")

        # Check if properties, geometry, and earthquake_id exist
        if earthquake_id and properties and geometry:
            title = properties.get("title")
            coordinates = geometry.get("coordinates")

            # Ensure coordinates have the expected format
            if coordinates and len(coordinates) >= 2:
                earthquake_dict[str(earthquake_id)] = {
                    "title": title,
                    "coordinates": (
                        round(coordinates[1], 5),  # Latitude
                        round(coordinates[0], 5),  # Longitude
                    ),
                }

    return earthquake_dict


def find_near_earthquake(earthquake_dict: Dict[str, Dict[str, Tuple[float, float]]],
                        coords_1: Tuple[float, float], number_of_earthquakes: int = 10) -> Dict[int, str]:
    distance_dict = {}
    for earthquake_id, earthquake_metadata in earthquake_dict.items():
        coords_2 = earthquake_metadata.get("coordinates")
        calculate_distance = int(geopy.distance.geodesic(coords_1, coords_2).km)
        distance_dict[calculate_distance] = earthquake_id

    order_and_limit_distance_dict = sorted(distance_dict.items())[:number_of_earthquakes]
    near_earthquake_dict = {distance: earthquake_id for distance, earthquake_id in order_and_limit_distance_dict}
    return near_earthquake_dict


def display_near_earthquake(
    near_earthquake_dict: Dict[int, str],
    earthquake_dict: Dict[str, Dict[str, Tuple[float, float]]]
) -> Dict[str, float]:
    display_earthquake_dict = {}
    for earthquake_distance, earthquake_id in near_earthquake_dict.items():
        earthquake_data = earthquake_dict.get(str(earthquake_id))
        display_title = earthquake_data.get("title", "Unknown") if earthquake_data else "Unknown"
        display_distance = float(earthquake_distance)
        display_earthquake_dict[str(display_title)] = display_distance
    return display_earthquake_dict


def top_n_nearest_earthquakes(input_lat: float, input_lon: float, number_of_earthquakes: int = 10) -> Union[Dict[str, float], Dict[str, str]]:
    call_earthquake_api = api_response()
    if not call_earthquake_api:
        return {"error": "No data available from the API."}

    filter_earthquake_api_response = filter_api_response(earthquake_list=call_earthquake_api)
    get_near_earthquakes = find_near_earthquake(earthquake_dict=filter_earthquake_api_response,
                                                coords_1=(input_lat, input_lon), number_of_earthquakes=number_of_earthquakes)
    frontend_response = display_near_earthquake(near_earthquake_dict=get_near_earthquakes,
                                                earthquake_dict=filter_earthquake_api_response)
    return frontend_response