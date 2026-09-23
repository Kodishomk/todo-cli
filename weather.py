"""
Weather CLI Tool
----------------
A command-line application that fetches live weather data using the Open-Meteo API.
Demonstrates HTTP requests with the third-party `requests` library, JSON parsing,
and robust exception handling (`try/except`) for network failures and invalid API responses.
"""

import sys
import requests

# Open-Meteo Weather Code interpretation map
WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def get_coordinates(city_name: str) -> tuple[float, float, str, str] | None:
    """
    Converts a city name into (latitude, longitude, formatted_name, country)
    using the Open-Meteo Geocoding API.
    Returns None if the city is not found.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = data.get("results")

    if not results:
        return None

    top_match = results[0]
    lat = top_match["latitude"]
    lon = top_match["longitude"]
    name = top_match["name"]
    country = top_match.get("country", "")

    return lat, lon, name, country


def get_weather(lat: float, lon: float) -> dict:
    """
    Fetches current weather data (temperature, relative humidity, weathercode)
    from Open-Meteo for given coordinates.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code"],
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def fetch_and_display_weather(city_input: str) -> None:
    """Handles the network operations wrapped inside a try/except error guard."""
    try:
        # Step 1: Geocode city name to coordinates
        coords = get_coordinates(city_input)

        if not coords:
            print(f"\nError: City '{city_input}' not found. Please check the spelling and try again.")
            return

        lat, lon, formatted_name, country = coords

        # Step 2: Fetch current weather metrics
        weather_data = get_weather(lat, lon)
        current = weather_data.get("current", {})

        temp_c = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wmo_code = current.get("weather_code", 0)

        condition = WMO_WEATHER_CODES.get(wmo_code, "Unknown")

        # Step 3: Print result
        location_str = f"{formatted_name}, {country}" if country else formatted_name
        print("\n" + "=" * 40)
        print(f" Weather for: {location_str}")
        print("=" * 40)
        print(f" Temperature: {temp_c}°C ({ (temp_c * 9/5) + 32:.1f}°F)")
        print(f" Condition:   {condition}")
        print(f" Humidity:    {humidity}%")
        print("=" * 40)

    except requests.exceptions.Timeout:
        print("\nError: Connection timed out while contacting the weather service.")
    except requests.exceptions.ConnectionError:
        print("\nError: Couldn't reach the weather service. Please check your internet connection and try again.")
    except requests.exceptions.HTTPError as http_err:
        print(f"\nError: Weather service returned an HTTP error: {http_err}")
    except (KeyError, ValueError):
        print("\nError: Unable to parse response from weather service.")


def main() -> None:
    """Main application loop."""
    print("=== WEATHER CLI TOOL ===")

    while True:
        city = input("\nEnter a city name: ").strip()

        if not city:
            print("Error: City name cannot be left blank.")
            continue

        fetch_and_display_weather(city)

        # Loop prompt
        while True:
            choice = input("\nCheck another city? (y/n): ").strip().lower()
            if choice == "y":
                break
            elif choice == "n":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Please enter 'y' for Yes or 'n' for No.")


if __name__ == "__main__":
    main()