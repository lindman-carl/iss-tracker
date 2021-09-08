from sys import argv
import requests
import json
import webbrowser
from datetime import datetime


def get_url() -> str:
    """Gets url from command line arguments if there is any

    Returns:
        str: url to iss-api
    """

    if len(argv) > 0:
        url = "http://api.open-notify.org/iss-now.json"
    else:
        url = argv[1]
    return url


def get_iss_data(url: str) -> json:
    """Gets ISS data in the form of a json

    Args:
        url (str): Url of the iss json

    Returns:
        json: Containing timestamp, message, iss-coordinates
    """

    iss_json = requests.get(url)
    print(type(iss_json))
    return iss_json.json()


def get_iss_coordinates(data: json) -> tuple:
    """Extracts ISS-coordinates from API-data

    Args:
        data (json): API-data

    Returns:
        tuple: (latitude, longitude)
    """

    iss_position = data["iss_position"]
    return (iss_position["latitude"], iss_position["longitude"])


def open_google_maps(lat: str, long: str, zoom: int = 2):
    """Opens Google Maps in the system default webbrowser centered on the argument coordinates          

    Args:
        lat (str): Latitude position
        long (str): Longitude position
        zoom (int): Zoom level 0-21, 2 is default
    """

    url = f"https://www.google.com/maps/place/{lat}+{long}/@{lat},{long},{zoom}z"
    webbrowser.open(url)


def format_coordinates(lat: str, long: str) -> tuple:
    """This is an incorrect way of formatting coordinates

    Args:
        lat (str): latitude coordinates in ---- format
        long (str): longitude coordinates in ---- format

    Returns:
        tuple: formatted latitude, formatted longitude
    """

    lat_degrees = lat.split(".")[0].strip("-")
    lat_minutes = lat.split(".")[1][0:2]
    lat_seconds = lat.split(".")[1][2:]

    if lat[0] == "-":
        lat_ns = "N"
    else:
        lat_ns = "S"

    long_degrees = long.split(".")[0].strip("-")
    long_minutes = long.split(".")[1][0:2]
    long_seconds = long.split(".")[1][2:]

    if long[0] == "-":
        long_ws = "W"
    else:
        long_ws = "E"

    formatted_lat = f"{lat_degrees}\N{DEGREE SIGN}{lat_minutes}\'{lat_seconds}\" {lat_ns}"
    formatted_long = f"{long_degrees}\N{DEGREE SIGN}{long_minutes}\'{long_seconds}\" {long_ws}"

    return (formatted_lat, formatted_long)


def main():
    url = get_url()
    iss_data = get_iss_data(url)
    iss_lat, iss_long = get_iss_coordinates(iss_data)
    timestamp = datetime.fromtimestamp(float(iss_data["timestamp"]))
    # formatted_lat, formatted_long = format_coordinates(iss_lat, iss_long)

    print(
        f"ISS-Position ({timestamp})\nLatitude:  {iss_lat}\nLongitude: {iss_long}")
    open_google_maps(iss_lat, iss_long)


if __name__ == "__main__":
    main()
