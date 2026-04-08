"""
Weather Data Collection Module
Fetches weather data from OpenWeatherMap API
"""

import requests
from typing import Dict, Optional

# Get your free API key from: https://openweathermap.org/api
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_data(location: str, api_key: str = API_KEY) -> Dict:
    """
    Fetch weather data for a given location.
    
    Args:
        location: City name (e.g., "Mumbai", "Chennai")
        api_key: OpenWeatherMap API key
    
    Returns:
        Dictionary containing weather parameters
    """
    try:
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # For Celsius and km/h
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant weather parameters
        weather_data = {
            "location": data.get("name", location),
            "wind_speed": data["wind"]["speed"] * 3.6,  # Convert m/s to km/h
            "wind_direction": data["wind"].get("deg", 0),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "visibility": data.get("visibility", 10000) / 1000,  # Convert to km
            "clouds": data["clouds"]["all"],  # Cloud coverage percentage
        }
        
        # Check for rain/storm data
        if "rain" in data:
            weather_data["rain_1h"] = data["rain"].get("1h", 0)
        else:
            weather_data["rain_1h"] = 0
            
        return weather_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        return None


def get_marine_forecast(lat: float, lon: float, api_key: str = API_KEY) -> Optional[Dict]:
    """
    Get marine-specific forecast data (requires One Call API subscription).
    
    Args:
        lat: Latitude
        lon: Longitude
        api_key: OpenWeatherMap API key
    
    Returns:
        Dictionary with marine forecast data
    """
    try:
        url = "https://api.openweathermap.org/data/2.5/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "exclude": "minutely,hourly"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract alerts if any
        alerts = data.get("alerts", [])
        
        return {
            "current": data.get("current", {}),
            "daily": data.get("daily", []),
            "alerts": alerts
        }
        
    except Exception as e:
        print(f"Error fetching marine forecast: {e}")
        return None


# For testing without API key
def get_mock_weather_data(location: str, scenario: str = "normal") -> Dict:
    """
    Generate mock weather data for testing.
    
    Args:
        location: City name
        scenario: "normal", "windy", "storm", "heavy_rain"
    
    Returns:
        Mock weather data dictionary
    """
    scenarios = {
        "normal": {
            "wind_speed": 15,
            "temperature": 28,
            "condition": "Clear",
            "description": "clear sky",
            "rain_1h": 0,
            "visibility": 10,
            "humidity": 65,
            "clouds": 20
        },
        "windy": {
            "wind_speed": 35,
            "temperature": 25,
            "condition": "Clouds",
            "description": "scattered clouds",
            "rain_1h": 0,
            "visibility": 8,
            "humidity": 70,
            "clouds": 45
        },
        "storm": {
            "wind_speed": 55,
            "temperature": 22,
            "condition": "Thunderstorm",
            "description": "thunderstorm with heavy rain",
            "rain_1h": 25,
            "visibility": 2,
            "humidity": 95,
            "clouds": 100
        },
        "heavy_rain": {
            "wind_speed": 28,
            "temperature": 24,
            "condition": "Rain",
            "description": "heavy intensity rain",
            "rain_1h": 15,
            "visibility": 4,
            "humidity": 90,
            "clouds": 90
        }
    }
    
    data = scenarios.get(scenario, scenarios["normal"])
    data["location"] = location
    data["pressure"] = 1013
    data["wind_direction"] = 180
    
    return data


if __name__ == "__main__":
    # Test with mock data
    print("Testing with mock data:")
    for scenario in ["normal", "windy", "storm", "heavy_rain"]:
        data = get_mock_weather_data("Mumbai", scenario)
        print(f"\n{scenario.upper()}:")
        print(f"  Wind: {data['wind_speed']} km/h")
        print(f"  Condition: {data['condition']}")
        print(f"  Rain: {data['rain_1h']} mm/h")
