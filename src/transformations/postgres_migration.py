import json
import pandas as pd  # type: ignore
import re


def extract_city(title):
    # Regular expression to find the substring after the last comma
    match = re.search(r',\s*(.+)$', title)
    if match:
        return match.group(1).strip()  # Return the matched city name
    return None  # Return None if no match is found


with open("earthquake_summary.json", 'r') as file:
    data = json.load(file)

records = []

for id, details in data.items():
    record = {
        "ID": id,
        "City": extract_city(details["title"]),
        "Latitude": details["coordinates"][0],
        "Longitude": details["coordinates"][1],
    }
    records.append(record)

df = pd.DataFrame(records)
