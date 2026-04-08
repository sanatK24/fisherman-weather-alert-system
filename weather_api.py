import requests
from typing import Dict, Optional, Tuple

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"


def _map_open_meteo_weather_code(weather_code: int) -> Tuple[str, str]:
    mapping = {
        0: ("Clear", "clear sky"),
        1: ("Clouds", "mainly clear"),
        2: ("Clouds", "partly cloudy"),
        3: ("Clouds", "overcast"),
        45: ("Fog", "fog"),
        48: ("Fog", "depositing rime fog"),
        51: ("Drizzle", "light drizzle"),
        53: ("Drizzle", "moderate drizzle"),
        55: ("Drizzle", "dense drizzle"),
        56: ("Drizzle", "freezing drizzle"),
        57: ("Drizzle", "dense freezing drizzle"),
        61: ("Rain", "slight rain"),
        63: ("Rain", "moderate rain"),
        65: ("Rain", "heavy rain"),
        66: ("Rain", "freezing rain"),
        67: ("Rain", "heavy freezing rain"),
        71: ("Snow", "slight snow fall"),
        73: ("Snow", "moderate snow fall"),
        75: ("Snow", "heavy snow fall"),
        77: ("Snow", "snow grains"),
        80: ("Rain", "slight rain showers"),
        81: ("Rain", "moderate rain showers"),
        82: ("Rain", "violent rain showers"),
        85: ("Snow", "slight snow showers"),
        86: ("Snow", "heavy snow showers"),
        95: ("Thunderstorm", "thunderstorm"),
        96: ("Thunderstorm", "thunderstorm with hail"),
        99: ("Thunderstorm", "heavy thunderstorm with hail"),
    }
    return mapping.get(weather_code, ("Clouds", "partly cloudy"))


def _has_real_api_key(api_key: str) -> bool:
    return bool(api_key and api_key != "YOUR_API_KEY_HERE")


def _geocode_location(location: str) -> Optional[Dict]:
    """Convert city name to lat/lon using Open-Meteo Geocoding API (free, no key)."""
    try:
        geo_params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        geo_response = requests.get(OPEN_METEO_GEOCODE_URL, params=geo_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        results = geo_data.get("results", [])
        if not results:
            print(f"Location not found: {location}")
            return None
        place = results[0]
        return {
            "name": place.get("name", location),
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "country": place.get("country", "")
        }
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None


def get_ocean_data(lat: float, lon: float) -> Optional[Dict]:
    """Fetch real ocean/marine data from Open-Meteo Marine API (free, no key)."""
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ",".join([
                "wave_height",
                "wave_direction",
                "wave_period",
                "wind_wave_height",
                "wind_wave_period",
                "swell_wave_height",
                "swell_wave_direction",
                "swell_wave_period",
                "ocean_current_velocity",
                "ocean_current_direction",
            ])
        }
        response = requests.get(OPEN_METEO_MARINE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})

        return {
            "wave_height": float(current.get("wave_height", 0)),
            "wave_direction": float(current.get("wave_direction", 0)),
            "wave_period": float(current.get("wave_period", 0)),
            "wind_wave_height": float(current.get("wind_wave_height", 0)),
            "wind_wave_period": float(current.get("wind_wave_period", 0)),
            "swell_wave_height": float(current.get("swell_wave_height", 0)),
            "swell_wave_direction": float(current.get("swell_wave_direction", 0)),
            "swell_wave_period": float(current.get("swell_wave_period", 0)),
            "ocean_current_velocity": float(current.get("ocean_current_velocity", 0)),
            "ocean_current_direction": float(current.get("ocean_current_direction", 0)),
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ocean data: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error parsing ocean data: {e}")
        return None


def get_weather_data(location: str, api_key: str = API_KEY) -> Dict:
    """Fetch real weather + ocean data for a location. Uses free APIs (no key needed)."""
    try:
        # Step 1: Geocode the location
        geo = _geocode_location(location)
        if geo is None:
            return None

        lat = geo["latitude"]
        lon = geo["longitude"]

        # Step 2: Get atmospheric weather data from Open-Meteo
        if _has_real_api_key(api_key):
            params = {
                "q": location,
                "appid": api_key,
                "units": "metric"
            }
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

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
                "clouds": data["clouds"]["all"],
                "rain_1h": data.get("rain", {}).get("1h", 0),
            }
        else:
            # Free no-key fallback: Open-Meteo
            forecast_params = {
                "latitude": lat,
                "longitude": lon,
                "current": ",".join([
                    "temperature_2m",
                    "relative_humidity_2m",
                    "pressure_msl",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "weather_code",
                    "cloud_cover",
                    "visibility",
                    "precipitation",
                ])
            }
            forecast_response = requests.get(OPEN_METEO_FORECAST_URL, params=forecast_params, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            current = forecast_data.get("current", {})

            weather_code = int(current.get("weather_code", 2))
            condition, description = _map_open_meteo_weather_code(weather_code)
            visibility_m = current.get("visibility")

            weather_data = {
                "location": geo["name"],
                "wind_speed": float(current.get("wind_speed_10m", 0)),
                "wind_direction": float(current.get("wind_direction_10m", 0)),
                "temperature": float(current.get("temperature_2m", 0)),
                "humidity": float(current.get("relative_humidity_2m", 0)),
                "pressure": float(current.get("pressure_msl", 1013)),
                "condition": condition,
                "description": description,
                "visibility": (float(visibility_m) / 1000) if visibility_m is not None else 10,
                "clouds": float(current.get("cloud_cover", 0)),
                "rain_1h": float(current.get("precipitation", 0)),
            }

        # Step 3: Get ocean/marine data
        ocean = get_ocean_data(lat, lon)
        if ocean:
            weather_data.update(ocean)
        else:
            # Provide defaults if ocean data unavailable (e.g. inland city)
            weather_data.update({
                "wave_height": 0,
                "wave_period": 0,
                "swell_wave_height": 0,
                "swell_wave_period": 0,
                "ocean_current_velocity": 0,
            })

        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error parsing weather data: {e}")
        return None


def get_marine_forecast(lat: float, lon: float, api_key: str = API_KEY) -> Optional[Dict]:
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






if __name__ == "__main__":
    print("Testing Weather API with REAL data...\n")

    test_cities = ["Mumbai", "Chennai", "Kochi", "Goa"]

    for city in test_cities:
        print(f"\n{city}:")
        data = get_weather_data(city)
        if data:
            print(f"  Wind: {data['wind_speed']:.1f} km/h")
            print(f"  Temp: {data['temperature']:.1f} C")
            print(f"  Condition: {data['condition']} ({data['description']})")
            print(f"  Visibility: {data['visibility']:.1f} km")
            print(f"  Rain: {data['rain_1h']:.1f} mm/h")
            print(f"  Wave Height: {data.get('wave_height', 0):.2f} m")
            print(f"  Swell Height: {data.get('swell_wave_height', 0):.2f} m")
            print(f"  Wave Period: {data.get('wave_period', 0):.1f} s")
            print(f"  Ocean Current: {data.get('ocean_current_velocity', 0):.2f} km/h")
        else:
            print("  Failed to fetch data")
