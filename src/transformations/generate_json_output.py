import json
from src.transformations.earthquake import api_response, filter_api_response
from typing import Dict, Tuple, Union
import os


def extract_earthquake_title_and_coordinates() -> Union[Dict[str, Dict[str, Tuple[float, float]]], Dict[str, str]]:
    """Extract earthquake title and coordinates based on json response from public API.

    Returns:
        Union[Dict[str, Dict[str, Tuple[float, float]]], Dict[str, str]]: public earthquake API json results.
    """
    call_earthquake_api = api_response()
    if not call_earthquake_api:
        return {"error": "No data available from the API."}

    filter_earthquake_api_response = filter_api_response(earthquake_list=call_earthquake_api)

    return filter_earthquake_api_response


def save_json_to_file(data: Union[Dict[str, Dict[str, Tuple[float, float]]], Dict[str, str]], filename: str) -> None:
    """Save a dictionary as a JSON file.

    Args:
        data (Union[Dict[str, Dict[str, Tuple[float, float]]], Dict[str, str]]): Data to be saved.
        filename (str): Name of the file to be saved
    """
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    """Drive program."""

    base_dict_earthquake = extract_earthquake_title_and_coordinates()

    if isinstance(base_dict_earthquake, Dict):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        json_file_path = os.path.join(project_root, "earthquake_summary.json")

        save_json_to_file(base_dict_earthquake, json_file_path)
