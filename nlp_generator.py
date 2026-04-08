"""
NLP Message Generator Module
Generates human-friendly, natural language alerts with multi-language support
"""

from typing import Dict, Optional
from alert_engine import AlertLevel


# Message templates for different alert levels
TEMPLATES = {
    "en": {
        AlertLevel.SAFE: [
            "Great news! The weather is perfect for fishing today in {location}. "
            "With winds at {wind_speed:.0f} km/h and {condition} skies, you can safely head out to sea.",
            
            "Good conditions for fishing in {location}! "
            "Wind speed is just {wind_speed:.0f} km/h. Enjoy your catch!",
            
            "The sea looks calm near {location}. "
            "With visibility of {visibility:.0f} km and gentle winds, it's a good day to fish."
        ],
        AlertLevel.CAUTION: [
            "⚠️ Attention fishermen in {location}! Weather conditions require caution today. "
            "Wind speed is {wind_speed:.0f} km/h with {condition}. "
            "If you go fishing, stay close to shore and keep monitoring the weather.",
            
            "⚠️ Moderate weather alert for {location}. "
            "Winds are picking up at {wind_speed:.0f} km/h. "
            "Consider shorter fishing trips and stay alert.",
            
            "⚠️ Be careful if fishing near {location} today. "
            "Conditions are not ideal with {condition} and {wind_speed:.0f} km/h winds. "
            "Experienced fishermen only."
        ],
        AlertLevel.DANGEROUS: [
            "🚫 DANGER! Do NOT go fishing today in {location}! "
            "Severe weather with {wind_speed:.0f} km/h winds and {condition}. "
            "Stay on shore until conditions improve.",
            
            "🚫 EMERGENCY ALERT for {location}! Extremely dangerous conditions at sea. "
            "Wind speed: {wind_speed:.0f} km/h. Visibility: {visibility:.0f} km. "
            "All fishing activities should be suspended.",
            
            "🚫 WARNING: Life-threatening weather near {location}! "
            "{condition} with winds up to {wind_speed:.0f} km/h. "
            "Do not venture into the sea under any circumstances."
        ]
    },
    "hi": {  # Hindi
        AlertLevel.SAFE: [
            "अच्छी खबर! {location} में मछली पकड़ने के लिए मौसम बिल्कुल सही है। "
            "हवा की गति {wind_speed:.0f} km/h है। सुरक्षित रूप से समुद्र में जा सकते हैं।",
            
            "{location} में मछली पकड़ने की अच्छी स्थिति! "
            "हवा की गति केवल {wind_speed:.0f} km/h है। अच्छी मछली पकड़ें!"
        ],
        AlertLevel.CAUTION: [
            "⚠️ {location} के मछुआरों को सूचना! आज मौसम में सावधानी बरतें। "
            "हवा की गति {wind_speed:.0f} km/h है। किनारे के पास रहें।",
            
            "⚠️ {location} के लिए सतर्कता! "
            "हवाएं तेज हो रही हैं - {wind_speed:.0f} km/h। सावधान रहें।"
        ],
        AlertLevel.DANGEROUS: [
            "🚫 खतरा! आज {location} में मछली पकड़ने न जाएं! "
            "भयंकर मौसम - हवा {wind_speed:.0f} km/h। किनारे पर रहें।",
            
            "🚫 आपातकालीन चेतावनी! {location} में बेहद खतरनाक स्थिति। "
            "समुद्र में न जाएं!"
        ]
    },
    "mr": {  # Marathi
        AlertLevel.SAFE: [
            "चांगली बातमी! {location} मध्ये मासेमारीसाठी हवामान उत्तम आहे। "
            "वाऱ्याचा वेग {wind_speed:.0f} km/h आहे। सुखरूप समुद्रात जा.",
            
            "{location} मध्ये मासेमारीसाठी चांगली परिस्थिती! "
            "वाऱ्याचा वेग फक्त {wind_speed:.0f} km/h आहे."
        ],
        AlertLevel.CAUTION: [
            "⚠️ {location} मधील मच्छीमारांनो सावधान! आज हवामान काळजी घ्या. "
            "वाऱ्याचा वेग {wind_speed:.0f} km/h आहे। किनाऱ्याजवळ राहा.",
            
            "⚠️ {location} साठी सतर्कता! "
            "वारे वाढत आहेत - {wind_speed:.0f} km/h. सावध राहा."
        ],
        AlertLevel.DANGEROUS: [
            "🚫 धोका! आज {location} मध्ये मासेमारीला जाऊ नका! "
            "भयंकर हवामान - वारा {wind_speed:.0f} km/h. किनाऱ्यावर राहा.",
            
            "🚫 आपत्कालीन इशारा! {location} मध्ये अत्यंत धोकादायक परिस्थिती। "
            "समुद्रात जाऊ नका!"
        ]
    }
}


def generate_nlp_message(
    weather_data: Dict, 
    alert_level: AlertLevel,
    language: str = "en",
    template_index: int = 0
) -> str:
    """
    Generate a natural language alert message.
    
    Args:
        weather_data: Dictionary containing weather parameters
        alert_level: The determined alert level
        language: Language code ("en", "hi", "mr")
        template_index: Which template variant to use (0, 1, or 2)
    
    Returns:
        Human-friendly alert message string
    """
    # Get templates for the language, fallback to English
    lang_templates = TEMPLATES.get(language, TEMPLATES["en"])
    level_templates = lang_templates.get(alert_level, lang_templates[AlertLevel.CAUTION])
    
    # Select template (with bounds checking)
    template_index = template_index % len(level_templates)
    template = level_templates[template_index]
    
    # Format the template with weather data
    try:
        message = template.format(
            location=weather_data.get("location", "your area"),
            wind_speed=weather_data.get("wind_speed", 0),
            temperature=weather_data.get("temperature", 25),
            condition=weather_data.get("condition", "unknown conditions"),
            description=weather_data.get("description", ""),
            visibility=weather_data.get("visibility", 10),
            humidity=weather_data.get("humidity", 50),
            rain_1h=weather_data.get("rain_1h", 0)
        )
    except KeyError:
        # Fallback to simple message
        message = f"Weather alert for {weather_data.get('location', 'your area')}. "
        message += f"Wind: {weather_data.get('wind_speed', 0):.0f} km/h."
    
    return message


def generate_sms_alert(weather_data: Dict, alert_level: AlertLevel, language: str = "en") -> str:
    """
    Generate a short SMS-friendly alert (max 160 characters).
    
    Args:
        weather_data: Weather data dictionary
        alert_level: Alert severity level
        language: Language code
    
    Returns:
        Short alert message suitable for SMS
    """
    location = weather_data.get("location", "")[:15]  # Truncate location
    wind = weather_data.get("wind_speed", 0)
    
    sms_templates = {
        "en": {
            AlertLevel.SAFE: f"✅ {location}: Safe to fish. Wind {wind:.0f}km/h. Good conditions.",
            AlertLevel.CAUTION: f"⚠️ {location}: Caution! Wind {wind:.0f}km/h. Stay near shore.",
            AlertLevel.DANGEROUS: f"🚫 {location}: DANGER! Wind {wind:.0f}km/h. DO NOT go to sea!"
        },
        "hi": {
            AlertLevel.SAFE: f"✅ {location}: मछली पकड़ना सुरक्षित। हवा {wind:.0f}km/h।",
            AlertLevel.CAUTION: f"⚠️ {location}: सावधान! हवा {wind:.0f}km/h। किनारे पर रहें।",
            AlertLevel.DANGEROUS: f"🚫 {location}: खतरा! हवा {wind:.0f}km/h। समुद्र में न जाएं!"
        },
        "mr": {
            AlertLevel.SAFE: f"✅ {location}: मासेमारी सुरक्षित. वारा {wind:.0f}km/h.",
            AlertLevel.CAUTION: f"⚠️ {location}: सावध! वारा {wind:.0f}km/h. किनाऱ्यावर राहा.",
            AlertLevel.DANGEROUS: f"🚫 {location}: धोका! वारा {wind:.0f}km/h. समुद्रात जाऊ नका!"
        }
    }
    
    lang_sms = sms_templates.get(language, sms_templates["en"])
    return lang_sms.get(alert_level, lang_sms[AlertLevel.CAUTION])


def generate_voice_text(weather_data: Dict, alert_level: AlertLevel, language: str = "en") -> str:
    """
    Generate text optimized for text-to-speech conversion.
    Uses simpler sentences, numbers spelled out for clarity.
    
    Args:
        weather_data: Weather data dictionary
        alert_level: Alert severity level
        language: Language code
    
    Returns:
        Text suitable for TTS conversion
    """
    location = weather_data.get("location", "your area")
    wind = int(weather_data.get("wind_speed", 0))
    
    if language == "en":
        if alert_level == AlertLevel.DANGEROUS:
            return (
                f"Attention! Danger alert for {location}. "
                f"Wind speed is {wind} kilometers per hour. "
                "Do not go fishing today. Stay safe on shore."
            )
        elif alert_level == AlertLevel.CAUTION:
            return (
                f"Caution alert for {location}. "
                f"Wind speed is {wind} kilometers per hour. "
                "Be careful if you go fishing. Stay close to the shore."
            )
        else:
            return (
                f"Good news for fishermen in {location}. "
                f"Wind speed is only {wind} kilometers per hour. "
                "It is safe to go fishing today."
            )
    elif language == "hi":
        if alert_level == AlertLevel.DANGEROUS:
            return (
                f"ध्यान दें! {location} के लिए खतरे की चेतावनी। "
                f"हवा की गति {wind} किलोमीटर प्रति घंटा है। "
                "आज मछली पकड़ने न जाएं। किनारे पर सुरक्षित रहें।"
            )
        elif alert_level == AlertLevel.CAUTION:
            return (
                f"{location} के लिए सावधानी की चेतावनी। "
                f"हवा की गति {wind} किलोमीटर प्रति घंटा है। "
                "अगर मछली पकड़ने जाएं तो सावधान रहें।"
            )
        else:
            return (
                f"{location} के मछुआरों के लिए अच्छी खबर। "
                f"हवा की गति केवल {wind} किलोमीटर प्रति घंटा है। "
                "आज मछली पकड़ने जाना सुरक्षित है।"
            )
    
    # Fallback to English
    return generate_voice_text(weather_data, alert_level, "en")


if __name__ == "__main__":
    # Test NLP message generation
    from weather_api import get_mock_weather_data
    from alert_engine import generate_alert
    
    print("Testing NLP Message Generator")
    print("=" * 60)
    
    test_cases = [
        ("Mumbai", "normal", AlertLevel.SAFE),
        ("Chennai", "windy", AlertLevel.CAUTION),
        ("Kochi", "storm", AlertLevel.DANGEROUS)
    ]
    
    for location, scenario, expected_level in test_cases:
        weather = get_mock_weather_data(location, scenario)
        
        print(f"\n📍 {location} ({scenario}):")
        print("-" * 40)
        
        for lang in ["en", "hi", "mr"]:
            print(f"\n[{lang.upper()}]")
            print(generate_nlp_message(weather, expected_level, lang))
            print(f"\nSMS: {generate_sms_alert(weather, expected_level, lang)}")
