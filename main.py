from urllib import request
from datetime import datetime
import sys
import json
import webbrowser


def get_api_url() -> str:
    """Gets url from command line arguments if there is any

    Returns:
        str: url to iss-api
    """

    if len(sys.argv) > 0:
        url = "http://api.open-notify.org/iss-now.json"
    else:
        url = sys.argv[1]
    return url


def get_iss_data(url: str) -> json:
    """Gets ISS data in the form of a json

    Args:
        url (str): Url of the iss json

    Returns:
        json: Containing timestamp, message, iss-coordinates
    """

    # Gets API data and load json
    iss_request = request.urlopen(url)
    iss_json = json.load(iss_request)
    return iss_json


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


def format_coordinates_dms(lat: str, long: str) -> tuple:
    """Formats decimal degrees into DMS (Degrees, Minutes, Seconds)

    Args:
        lat (str): latitude coordinates in decimal degrees
        long (str): longitude coordinates in decimal degrees

    Returns:
        tuple: formatted latitude (DMS), formatted longitude (DMS)
    """

    # TODO: Make this shit sexier
    # Degrees are the whole number in decimal degrees
    lat_degrees = lat.split(".")[0].strip("-")
    lat_decimals = float("0." + lat.split(".")[1])
    # Minutes are derived from multiplying the decimals of the degrees by 60
    lat_minutes = str(lat_decimals * 60).split(".")
    lat_decimals = float("0." + lat_minutes[1])
    # Seconds are derived from multiplying the decimals of the minutes by 60
    lat_seconds = str(lat_decimals * 60).split(".")[0]

    # If the latitude decimal degree is negative then the coordinates are south of the ecuator
    if lat[0] == "-":
        lat_ns = "S"
    else:
        lat_ns = "N"

    # Degrees are the whole number in decimal degrees
    long_degrees = long.split(".")[0].strip("-")
    long_decimals = float("0." + long.split(".")[1])
    # Minutes are derived from multiplying the decimals of the degrees by 60
    long_minutes = str(long_decimals * 60).split(".")
    long_decimals = float("0." + long_minutes[1])
    # Seconds are derived from multiplying the decimals of the minutes by 60
    long_seconds = str(long_decimals * 60).split(".")[0]

    # If the longitude deciaml degree is negative the coordinates are west of the Greenwich prime meridian
    if long[0] == "-":
        long_ws = "W"
    else:
        long_ws = "E"

    formatted_lat = f"{lat_degrees}\N{DEGREE SIGN}{lat_minutes[0]}\'{lat_seconds}\" {lat_ns}"
    formatted_long = f"{long_degrees}\N{DEGREE SIGN}{long_minutes[0]}\'{long_seconds}\" {long_ws}"

    return (formatted_lat, formatted_long)


def print_iss_coordinates(latitude: str, longitude: str, timestamp: str) -> None:
    print(
        f"ISS-Coordinates ({timestamp})\n"
        f"Latitude:  {latitude}\n"
        f"Longitude: {longitude}")


def main():
    api_url = get_api_url()
    iss_data = get_iss_data(api_url)
    iss_lat, iss_long = get_iss_coordinates(iss_data)
    timestamp = datetime.fromtimestamp(float(iss_data["timestamp"]))
    formatted_lat, formatted_long = format_coordinates_dms(iss_lat, iss_long)

    print_iss_coordinates(formatted_lat, formatted_long, timestamp)
    open_google_maps(iss_lat, iss_long)


if __name__ == "__main__":
    main()
