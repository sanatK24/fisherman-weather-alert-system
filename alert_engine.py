"""
Alert Engine Module
Rule-based system for generating fishing safety alerts
"""

from typing import Dict, Tuple
from enum import Enum


class AlertLevel(Enum):
    """Alert severity levels"""
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"


# Safety thresholds for fishing
THRESHOLDS = {
    "wind_speed": {
        "safe": 20,       # Below 20 km/h is safe
        "caution": 35,    # 20-35 km/h requires caution
        "dangerous": 35   # Above 35 km/h is dangerous
    },
    "visibility": {
        "safe": 5,        # Above 5 km is safe
        "caution": 2,     # 2-5 km requires caution
        "dangerous": 2    # Below 2 km is dangerous
    },
    "rain_1h": {
        "safe": 2,        # Below 2 mm/h is safe
        "caution": 10,    # 2-10 mm/h requires caution
        "dangerous": 10   # Above 10 mm/h is dangerous
    }
}

# Dangerous weather conditions
DANGEROUS_CONDITIONS = ["Thunderstorm", "Tornado", "Hurricane", "Squall"]
CAUTION_CONDITIONS = ["Rain", "Drizzle", "Mist", "Fog"]


def analyze_wind(wind_speed: float) -> Tuple[AlertLevel, str]:
    """Analyze wind speed and return alert level with reason."""
    if wind_speed >= THRESHOLDS["wind_speed"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"High wind speed ({wind_speed:.1f} km/h)"
    elif wind_speed >= THRESHOLDS["wind_speed"]["safe"]:
        return AlertLevel.CAUTION, f"Moderate wind ({wind_speed:.1f} km/h)"
    else:
        return AlertLevel.SAFE, f"Low wind ({wind_speed:.1f} km/h)"


def analyze_visibility(visibility: float) -> Tuple[AlertLevel, str]:
    """Analyze visibility and return alert level with reason."""
    if visibility <= THRESHOLDS["visibility"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"Very poor visibility ({visibility:.1f} km)"
    elif visibility <= THRESHOLDS["visibility"]["safe"]:
        return AlertLevel.CAUTION, f"Reduced visibility ({visibility:.1f} km)"
    else:
        return AlertLevel.SAFE, f"Good visibility ({visibility:.1f} km)"


def analyze_rain(rain_1h: float) -> Tuple[AlertLevel, str]:
    """Analyze rainfall and return alert level with reason."""
    if rain_1h >= THRESHOLDS["rain_1h"]["dangerous"]:
        return AlertLevel.DANGEROUS, f"Heavy rainfall ({rain_1h:.1f} mm/h)"
    elif rain_1h >= THRESHOLDS["rain_1h"]["safe"]:
        return AlertLevel.CAUTION, f"Moderate rainfall ({rain_1h:.1f} mm/h)"
    else:
        return AlertLevel.SAFE, "No significant rainfall"


def analyze_condition(condition: str) -> Tuple[AlertLevel, str]:
    """Analyze weather condition and return alert level with reason."""
    if condition in DANGEROUS_CONDITIONS:
        return AlertLevel.DANGEROUS, f"Severe weather: {condition}"
    elif condition in CAUTION_CONDITIONS:
        return AlertLevel.CAUTION, f"Adverse weather: {condition}"
    else:
        return AlertLevel.SAFE, f"Weather: {condition}"


def generate_alert(weather_data: Dict) -> Dict:
    """
    Generate comprehensive fishing safety alert based on weather data.
    
    Args:
        weather_data: Dictionary containing weather parameters
    
    Returns:
        Dictionary with alert level, message, and detailed analysis
    """
    if weather_data is None:
        return {
            "level": AlertLevel.CAUTION,
            "icon": "⚠️",
            "title": "Weather Data Unavailable",
            "message": "Unable to fetch weather data. Please exercise caution.",
            "reasons": ["Could not retrieve current weather information"],
            "recommendation": "Check weather manually before going fishing."
        }
    
    # Analyze each parameter
    analyses = []
    
    wind_level, wind_reason = analyze_wind(weather_data.get("wind_speed", 0))
    analyses.append(("Wind", wind_level, wind_reason))
    
    visibility_level, visibility_reason = analyze_visibility(weather_data.get("visibility", 10))
    analyses.append(("Visibility", visibility_level, visibility_reason))
    
    rain_level, rain_reason = analyze_rain(weather_data.get("rain_1h", 0))
    analyses.append(("Rainfall", rain_level, rain_reason))
    
    condition_level, condition_reason = analyze_condition(weather_data.get("condition", "Clear"))
    analyses.append(("Condition", condition_level, condition_reason))
    
    # Determine overall alert level (highest severity wins)
    levels = [a[1] for a in analyses]
    
    if AlertLevel.DANGEROUS in levels:
        overall_level = AlertLevel.DANGEROUS
        icon = "🚫"
        title = "DANGEROUS - Do Not Go Fishing"
        recommendation = "Stay on shore. Conditions are too dangerous for fishing."
    elif AlertLevel.CAUTION in levels:
        overall_level = AlertLevel.CAUTION
        icon = "⚠️"
        title = "CAUTION - Be Careful"
        recommendation = "If you must go, stay close to shore and be alert."
    else:
        overall_level = AlertLevel.SAFE
        icon = "✅"
        title = "SAFE - Good for Fishing"
        recommendation = "Conditions are favorable. Enjoy your fishing!"
    
    # Collect reasons for non-safe conditions
    reasons = [
        f"{name}: {reason}" 
        for name, level, reason in analyses 
        if level != AlertLevel.SAFE
    ]
    
    if not reasons:
        reasons = ["All weather parameters are within safe limits"]
    
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
            "temperature": weather_data.get("temperature", 0)
        }
    }


def generate_summary_message(weather_data: Dict, level: AlertLevel) -> str:
    """Generate a human-friendly summary message."""
    location = weather_data.get("location", "your area")
    wind = weather_data.get("wind_speed", 0)
    condition = weather_data.get("condition", "").lower()
    
    if level == AlertLevel.DANGEROUS:
        return f"Dangerous conditions in {location}. Wind speed is {wind:.0f} km/h with {condition}. Fishing is NOT recommended today."
    elif level == AlertLevel.CAUTION:
        return f"Weather in {location} requires caution. Wind speed is {wind:.0f} km/h. Be careful if going fishing."
    else:
        return f"Weather in {location} is good for fishing. Wind speed is {wind:.0f} km/h with {condition}."


def format_alert_for_display(alert: Dict) -> str:
    """Format alert for terminal/SMS display."""
    lines = [
        f"\n{'='*50}",
        f"{alert['icon']} {alert['title']}",
        f"{'='*50}",
        f"📍 Location: {alert['location']}",
        f"\n{alert['message']}",
        f"\n📋 Details:"
    ]
    
    for reason in alert['reasons']:
        lines.append(f"  • {reason}")
    
    lines.extend([
        f"\n💡 Recommendation: {alert['recommendation']}",
        f"{'='*50}\n"
    ])
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test the alert engine
    from weather_api import get_mock_weather_data
    
    print("Testing Alert Engine")
    print("=" * 50)
    
    for scenario in ["normal", "windy", "storm", "heavy_rain"]:
        weather_data = get_mock_weather_data("Mumbai", scenario)
        alert = generate_alert(weather_data)
        print(format_alert_for_display(alert))
