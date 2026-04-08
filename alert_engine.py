from typing import Dict, Tuple
from enum import Enum


class AlertLevel(Enum):
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"



THRESHOLDS = {
    "wind_speed": {
        "safe": 20,
        "caution": 35,
        "dangerous": 35
    },
    "visibility": {
        "safe": 5,
        "caution": 2,
        "dangerous": 2
    },
    "rain_1h": {
        "safe": 2,
        "caution": 10,
        "dangerous": 10
    }
}

# Ocean thresholds (for small fishing boats)
OCEAN_THRESHOLDS = {
    "wave_height": {
        "safe": 1.0,       # < 1m is safe
        "caution": 2.5,    # 1-2.5m is caution
        "dangerous": 2.5   # > 2.5m is dangerous
    },
    "swell_wave_height": {
        "safe": 1.5,
        "caution": 3.0,
        "dangerous": 3.0
    },
    "ocean_current_velocity": {
        "safe": 2.0,       # < 2 km/h is safe
        "caution": 5.0,    # 2-5 km/h is caution
        "dangerous": 5.0   # > 5 km/h is dangerous
    }
}

DANGEROUS_CONDITIONS = ["Thunderstorm", "Tornado", "Hurricane", "Squall"]
CAUTION_CONDITIONS = ["Rain", "Drizzle", "Mist", "Fog"]


def analyze_wind(wind_speed: float) -> Tuple[AlertLevel, str]:
    if wind_speed >= THRESHOLDS["wind_speed"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"High wind speed ({wind_speed:.1f} km/h)"
    elif wind_speed >= THRESHOLDS["wind_speed"]["safe"]:
        return AlertLevel.CAUTION, f"Moderate wind ({wind_speed:.1f} km/h)"
    else:
        return AlertLevel.SAFE, f"Low wind ({wind_speed:.1f} km/h)"


def analyze_visibility(visibility: float) -> Tuple[AlertLevel, str]:
    if visibility <= THRESHOLDS["visibility"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"Very poor visibility ({visibility:.1f} km)"
    elif visibility <= THRESHOLDS["visibility"]["safe"]:
        return AlertLevel.CAUTION, f"Reduced visibility ({visibility:.1f} km)"
    else:
        return AlertLevel.SAFE, f"Good visibility ({visibility:.1f} km)"


def analyze_rain(rain_1h: float) -> Tuple[AlertLevel, str]:
    if rain_1h >= THRESHOLDS["rain_1h"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"Heavy rainfall ({rain_1h:.1f} mm/h)"
    elif rain_1h >= THRESHOLDS["rain_1h"]["safe"]:
        return AlertLevel.CAUTION, f"Moderate rainfall ({rain_1h:.1f} mm/h)"
    else:
        return AlertLevel.SAFE, "No significant rainfall"


def analyze_condition(condition: str) -> Tuple[AlertLevel, str]:
    if condition in DANGEROUS_CONDITIONS:
        return AlertLevel.DANGEROUS, f"Severe weather: {condition}"
    elif condition in CAUTION_CONDITIONS:
        return AlertLevel.CAUTION, f"Adverse weather: {condition}"
    else:
        return AlertLevel.SAFE, f"Weather: {condition}"


def analyze_waves(wave_height: float) -> Tuple[AlertLevel, str]:
    """Analyze wave height for fishing safety."""
    if wave_height >= OCEAN_THRESHOLDS["wave_height"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"High waves ({wave_height:.1f} m)"
    elif wave_height >= OCEAN_THRESHOLDS["wave_height"]["safe"]:
        return AlertLevel.CAUTION, f"Moderate waves ({wave_height:.1f} m)"
    else:
        return AlertLevel.SAFE, f"Calm sea ({wave_height:.1f} m waves)"


def analyze_swell(swell_height: float) -> Tuple[AlertLevel, str]:
    """Analyze swell wave height for fishing safety."""
    if swell_height >= OCEAN_THRESHOLDS["swell_wave_height"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"Heavy swell ({swell_height:.1f} m)"
    elif swell_height >= OCEAN_THRESHOLDS["swell_wave_height"]["safe"]:
        return AlertLevel.CAUTION, f"Moderate swell ({swell_height:.1f} m)"
    else:
        return AlertLevel.SAFE, f"Light swell ({swell_height:.1f} m)"


def analyze_current(velocity: float) -> Tuple[AlertLevel, str]:
    """Analyze ocean current velocity for fishing safety."""
    if velocity >= OCEAN_THRESHOLDS["ocean_current_velocity"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"Strong ocean current ({velocity:.1f} km/h)"
    elif velocity >= OCEAN_THRESHOLDS["ocean_current_velocity"]["safe"]:
        return AlertLevel.CAUTION, f"Moderate ocean current ({velocity:.1f} km/h)"
    else:
        return AlertLevel.SAFE, f"Weak ocean current ({velocity:.1f} km/h)"


def generate_alert(weather_data: Dict) -> Dict:
    if weather_data is None:
        return {
            "level": AlertLevel.CAUTION,
            "icon": "[CAUTION]",
            "title": "Weather Data Unavailable",
            "message": "Unable to fetch weather data. Please exercise caution.",
            "reasons": ["Could not retrieve current weather information"],
            "recommendation": "Check weather manually before going fishing."
        }
    
    analyses = []

    # Atmospheric analysis
    wind_level, wind_reason = analyze_wind(weather_data.get("wind_speed", 0))
    analyses.append(("Wind", wind_level, wind_reason))
    
    visibility_level, visibility_reason = analyze_visibility(weather_data.get("visibility", 10))
    analyses.append(("Visibility", visibility_level, visibility_reason))
    
    rain_level, rain_reason = analyze_rain(weather_data.get("rain_1h", 0))
    analyses.append(("Rainfall", rain_level, rain_reason))
    
    condition_level, condition_reason = analyze_condition(weather_data.get("condition", "Clear"))
    analyses.append(("Condition", condition_level, condition_reason))

    # Ocean analysis
    wave_height = weather_data.get("wave_height", 0)
    if wave_height > 0:
        wave_level, wave_reason = analyze_waves(wave_height)
        analyses.append(("Waves", wave_level, wave_reason))

    swell_height = weather_data.get("swell_wave_height", 0)
    if swell_height > 0:
        swell_level, swell_reason = analyze_swell(swell_height)
        analyses.append(("Swell", swell_level, swell_reason))

    current_vel = weather_data.get("ocean_current_velocity", 0)
    if current_vel > 0:
        current_level, current_reason = analyze_current(current_vel)
        analyses.append(("Current", current_level, current_reason))

    levels = [a[1] for a in analyses]
    
    if AlertLevel.DANGEROUS in levels:
        overall_level = AlertLevel.DANGEROUS
        icon = "[DANGER]"
        title = "DANGEROUS - Do Not Go Fishing"
        recommendation = "Stay on shore. Conditions are too dangerous for fishing."
    elif AlertLevel.CAUTION in levels:
        overall_level = AlertLevel.CAUTION
        icon = "[CAUTION]"
        title = "CAUTION - Be Careful"
        recommendation = "If you must go, stay close to shore and be alert."
    else:
        overall_level = AlertLevel.SAFE
        icon = "[SAFE]"
        title = "SAFE - Good for Fishing"
        recommendation = "Conditions are favorable. Enjoy your fishing!"
    
    reasons = [
        f"{name}: {reason}" 
        for name, level, reason in analyses 
        if level != AlertLevel.SAFE
    ]
    
    if not reasons:
        reasons = ["All weather and ocean parameters are within safe limits"]
    
    return {
        "level": overall_level,
        "icon": icon,
        "title": title,
        "message": generate_summary_message(weather_data, overall_level),
        "reasons": reasons,
        "recommendation": recommendation,
        "location": weather_data.get("location", "Unknown"),
        "details": {
            "wind_speed": weather_data.get("wind_speed", 0),
            "visibility": weather_data.get("visibility", 10),
            "rain_1h": weather_data.get("rain_1h", 0),
            "condition": weather_data.get("condition", "Unknown"),
            "temperature": weather_data.get("temperature", 0),
            "wave_height": weather_data.get("wave_height", 0),
            "wave_period": weather_data.get("wave_period", 0),
            "swell_wave_height": weather_data.get("swell_wave_height", 0),
            "ocean_current_velocity": weather_data.get("ocean_current_velocity", 0),
        }
    }


def generate_summary_message(weather_data: Dict, level: AlertLevel) -> str:
    location = weather_data.get("location", "your area")
    wind = weather_data.get("wind_speed", 0)
    condition = weather_data.get("condition", "").lower()
    wave = weather_data.get("wave_height", 0)
    swell = weather_data.get("swell_wave_height", 0)
    
    if level == AlertLevel.DANGEROUS:
        msg = f"Dangerous conditions in {location}. Wind speed is {wind:.0f} km/h with {condition}."
        if wave > 0:
            msg += f" Waves are {wave:.1f}m high."
        msg += " Fishing is NOT recommended today."
        return msg
    elif level == AlertLevel.CAUTION:
        msg = f"Weather in {location} requires caution. Wind speed is {wind:.0f} km/h."
        if wave > 0:
            msg += f" Wave height is {wave:.1f}m."
        msg += " Be careful if going fishing."
        return msg
    else:
        msg = f"Weather in {location} is good for fishing. Wind speed is {wind:.0f} km/h with {condition}."
        if wave > 0:
            msg += f" Sea is calm with {wave:.1f}m waves."
        return msg


def format_alert_for_display(alert: Dict) -> str:
    lines = [
        f"\n{alert['icon']} {alert['title']}",
        f"Location: {alert['location']}",
        f"\n{alert['message']}",
        f"\nDetails:"
    ]
    
    for reason in alert['reasons']:
        lines.append(f"  * {reason}")

    # Show ocean data if available
    details = alert.get("details", {})
    lines.append(f"\nWeather:")
    lines.append(f"  Wind: {details.get('wind_speed', 0):.0f} km/h")
    lines.append(f"  Temperature: {details.get('temperature', 0):.0f} C")
    lines.append(f"  Visibility: {details.get('visibility', 10):.0f} km")
    lines.append(f"  Rainfall: {details.get('rain_1h', 0):.1f} mm/h")

    wave = details.get("wave_height", 0)
    if wave > 0:
        lines.append(f"\nOcean:")
        lines.append(f"  Wave Height: {wave:.2f} m")
        lines.append(f"  Swell Height: {details.get('swell_wave_height', 0):.2f} m")
        lines.append(f"  Wave Period: {details.get('wave_period', 0):.1f} s")
        lines.append(f"  Ocean Current: {details.get('ocean_current_velocity', 0):.2f} km/h")
    
    lines.append(f"\nRecommendation: {alert['recommendation']}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    from weather_api import get_weather_data
    
    print("Testing Alert Engine with REAL data\n")
    
    for city in ["Mumbai", "Chennai", "Kochi", "Goa"]:
        weather_data = get_weather_data(city)
        if weather_data:
            alert = generate_alert(weather_data)
            print(format_alert_for_display(alert))
        else:
            print(f"\nFailed to fetch data for {city}")

