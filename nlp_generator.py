from typing import Dict, Optional
from alert_engine import AlertLevel


# Message templates for different alert levels
TEMPLATES = {
    "en": {
        AlertLevel.SAFE: [
            "Great news! The weather is perfect for fishing today in {location}. "
            "With winds at {wind_speed:.0f} km/h and {condition} skies, you can safely head out to sea. "
            "Waves are {wave_height:.1f}m - sea is calm.",
            
            "Good conditions for fishing in {location}! "
            "Wind speed is just {wind_speed:.0f} km/h. Waves at {wave_height:.1f}m. Enjoy your catch!",
            
            "The sea looks calm near {location}. "
            "With visibility of {visibility:.0f} km, gentle winds, and {wave_height:.1f}m waves, it's a good day to fish."
        ],
        AlertLevel.CAUTION: [
            "Attention fishermen in {location}! Weather conditions require caution today. "
            "Wind speed is {wind_speed:.0f} km/h with {condition}. Waves are {wave_height:.1f}m high. "
            "If you go fishing, stay close to shore and keep monitoring the weather.",
            
            "Moderate weather alert for {location}. "
            "Winds are picking up at {wind_speed:.0f} km/h. Wave height is {wave_height:.1f}m. "
            "Consider shorter fishing trips and stay alert.",
            
            "Be careful if fishing near {location} today. "
            "Conditions are not ideal with {condition} and {wind_speed:.0f} km/h winds. "
            "Swell at {swell_wave_height:.1f}m. Experienced fishermen only."
        ],
        AlertLevel.DANGEROUS: [
            "DANGER! Do NOT go fishing today in {location}! "
            "Severe weather with {wind_speed:.0f} km/h winds and {condition}. "
            "Waves are {wave_height:.1f}m high. Stay on shore until conditions improve.",
            
            "EMERGENCY ALERT for {location}! Extremely dangerous conditions at sea. "
            "Wind speed: {wind_speed:.0f} km/h. Waves: {wave_height:.1f}m. Visibility: {visibility:.0f} km. "
            "All fishing activities should be suspended.",
            
            "WARNING: Life-threatening weather near {location}! "
            "{condition} with winds up to {wind_speed:.0f} km/h and {wave_height:.1f}m waves. "
            "Do not venture into the sea under any circumstances."
        ]
    },
    "hi": {  # Hindi
        AlertLevel.SAFE: [
            "अच्छी खबर! {location} में मछली पकड़ने के लिए मौसम बिल्कुल सही है। "
            "हवा की गति {wind_speed:.0f} km/h है। लहरें {wave_height:.1f}m - समुद्र शांत है।",
            
            "{location} में मछली पकड़ने की अच्छी स्थिति! "
            "हवा की गति केवल {wind_speed:.0f} km/h है। लहरें {wave_height:.1f}m। अच्छी मछली पकड़ें!"
        ],
        AlertLevel.CAUTION: [
            "{location} के मछुआरों को सूचना! आज मौसम में सावधानी बरतें। "
            "हवा की गति {wind_speed:.0f} km/h है। लहरें {wave_height:.1f}m ऊंची हैं। किनारे के पास रहें।",
            
            "{location} के लिए सतर्कता! "
            "हवाएं तेज हो रही हैं - {wind_speed:.0f} km/h। लहरें {wave_height:.1f}m। सावधान रहें।"
        ],
        AlertLevel.DANGEROUS: [
            "खतरा! आज {location} में मछली पकड़ने न जाएं! "
            "भयंकर मौसम - हवा {wind_speed:.0f} km/h। लहरें {wave_height:.1f}m ऊंची। किनारे पर रहें।",
            
            "आपातकालीन चेतावनी! {location} में बेहद खतरनाक स्थिति। "
            "लहरें {wave_height:.1f}m। समुद्र में न जाएं!"
        ]
    },
    "mr": {  # Marathi
        AlertLevel.SAFE: [
            "चांगली बातमी! {location} मध्ये मासेमारीसाठी हवामान उत्तम आहे। "
            "वाऱ्याचा वेग {wind_speed:.0f} km/h आहे। लाटा {wave_height:.1f}m - समुद्र शांत आहे.",
            
            "{location} मध्ये मासेमारीसाठी चांगली परिस्थिती! "
            "वाऱ्याचा वेग फक्त {wind_speed:.0f} km/h आहे। लाटा {wave_height:.1f}m."
        ],
        AlertLevel.CAUTION: [
            "{location} मधील मच्छीमारांनो सावधान! आज हवामान काळजी घ्या. "
            "वाऱ्याचा वेग {wind_speed:.0f} km/h आहे। लाटा {wave_height:.1f}m उंच। किनाऱ्याजवळ राहा.",
            
            "{location} साठी सतर्कता! "
            "वारे वाढत आहेत - {wind_speed:.0f} km/h। लाटा {wave_height:.1f}m. सावध राहा."
        ],
        AlertLevel.DANGEROUS: [
            "धोका! आज {location} मध्ये मासेमारीला जाऊ नका! "
            "भयंकर हवामान - वारा {wind_speed:.0f} km/h। लाटा {wave_height:.1f}m उंच. किनाऱ्यावर राहा.",
            
            "आपत्कालीन इशारा! {location} मध्ये अत्यंत धोकादायक परिस्थिती। "
            "लाटा {wave_height:.1f}m. समुद्रात जाऊ नका!"
        ]
    }
}


def generate_nlp_message(
    weather_data: Dict, 
    alert_level: AlertLevel,
    language: str = "en",
    template_index: int = 0
) -> str:
    lang_templates = TEMPLATES.get(language, TEMPLATES["en"])
    level_templates = lang_templates.get(alert_level, lang_templates[AlertLevel.CAUTION])
    
    template_index = template_index % len(level_templates)
    template = level_templates[template_index]
    
    try:
        message = template.format(
            location=weather_data.get("location", "your area"),
            wind_speed=weather_data.get("wind_speed", 0),
            temperature=weather_data.get("temperature", 25),
            condition=weather_data.get("condition", "unknown conditions"),
            description=weather_data.get("description", ""),
            visibility=weather_data.get("visibility", 10),
            humidity=weather_data.get("humidity", 50),
            rain_1h=weather_data.get("rain_1h", 0),
            wave_height=weather_data.get("wave_height", 0),
            wave_period=weather_data.get("wave_period", 0),
            swell_wave_height=weather_data.get("swell_wave_height", 0),
            ocean_current_velocity=weather_data.get("ocean_current_velocity", 0),
        )
    except KeyError:
        message = f"Weather alert for {weather_data.get('location', 'your area')}. "
        message += f"Wind: {weather_data.get('wind_speed', 0):.0f} km/h. "
        message += f"Waves: {weather_data.get('wave_height', 0):.1f}m."
    
    return message


def generate_sms_alert(weather_data: Dict, alert_level: AlertLevel, language: str = "en") -> str:
    location = weather_data.get("location", "")[:15]
    wind = weather_data.get("wind_speed", 0)
    wave = weather_data.get("wave_height", 0)
    
    sms_templates = {
        "en": {
            AlertLevel.SAFE: f"{location}: Safe to fish. Wind {wind:.0f}km/h. Waves {wave:.1f}m. Good conditions.",
            AlertLevel.CAUTION: f"{location}: Caution! Wind {wind:.0f}km/h. Waves {wave:.1f}m. Stay near shore.",
            AlertLevel.DANGEROUS: f"{location}: DANGER! Wind {wind:.0f}km/h. Waves {wave:.1f}m. DO NOT go to sea!"
        },
        "hi": {
            AlertLevel.SAFE: f"{location}: मछली पकड़ना सुरक्षित। हवा {wind:.0f}km/h। लहरें {wave:.1f}m।",
            AlertLevel.CAUTION: f"{location}: सावधान! हवा {wind:.0f}km/h। लहरें {wave:.1f}m। किनारे पर रहें।",
            AlertLevel.DANGEROUS: f"{location}: खतरा! हवा {wind:.0f}km/h। लहरें {wave:.1f}m। समुद्र में न जाएं!"
        },
        "mr": {
            AlertLevel.SAFE: f"{location}: मासेमारी सुरक्षित. वारा {wind:.0f}km/h. लाटा {wave:.1f}m.",
            AlertLevel.CAUTION: f"{location}: सावध! वारा {wind:.0f}km/h. लाटा {wave:.1f}m. किनाऱ्यावर राहा.",
            AlertLevel.DANGEROUS: f"{location}: धोका! वारा {wind:.0f}km/h. लाटा {wave:.1f}m. समुद्रात जाऊ नका!"
        }
    }
    
    lang_sms = sms_templates.get(language, sms_templates["en"])
    return lang_sms.get(alert_level, lang_sms[AlertLevel.CAUTION])


def generate_voice_text(weather_data: Dict, alert_level: AlertLevel, language: str = "en") -> str:
    location = weather_data.get("location", "your area")
    wind = int(weather_data.get("wind_speed", 0))
    wave = weather_data.get("wave_height", 0)
    
    if language == "en":
        if alert_level == AlertLevel.DANGEROUS:
            return (
                f"Attention! Danger alert for {location}. "
                f"Wind speed is {wind} kilometers per hour. "
                f"Wave height is {wave:.1f} meters. "
                "Do not go fishing today. Stay safe on shore."
            )
        elif alert_level == AlertLevel.CAUTION:
            return (
                f"Caution alert for {location}. "
                f"Wind speed is {wind} kilometers per hour. "
                f"Wave height is {wave:.1f} meters. "
                "Be careful if you go fishing. Stay close to the shore."
            )
        else:
            return (
                f"Good news for fishermen in {location}. "
                f"Wind speed is only {wind} kilometers per hour. "
                f"Waves are just {wave:.1f} meters. "
                "It is safe to go fishing today."
            )
    elif language == "hi":
        if alert_level == AlertLevel.DANGEROUS:
            return (
                f"ध्यान दें! {location} के लिए खतरे की चेतावनी। "
                f"हवा की गति {wind} किलोमीटर प्रति घंटा है। "
                f"लहरें {wave:.1f} मीटर ऊंची हैं। "
                "आज मछली पकड़ने न जाएं। किनारे पर सुरक्षित रहें।"
            )
        elif alert_level == AlertLevel.CAUTION:
            return (
                f"{location} के लिए सावधानी की चेतावनी। "
                f"हवा की गति {wind} किलोमीटर प्रति घंटा है। "
                f"लहरें {wave:.1f} मीटर हैं। "
                "अगर मछली पकड़ने जाएं तो सावधान रहें।"
            )
        else:
            return (
                f"{location} के मछुआरों के लिए अच्छी खबर। "
                f"हवा की गति केवल {wind} किलोमीटर प्रति घंटा है। "
                f"लहरें सिर्फ {wave:.1f} मीटर हैं। "
                "आज मछली पकड़ने जाना सुरक्षित है।"
            )
    
    return generate_voice_text(weather_data, alert_level, "en")


if __name__ == "__main__":
    from weather_api import get_weather_data
    from alert_engine import generate_alert
    
    print("Testing NLP Message Generator with REAL data\n")
    
    for city in ["Mumbai", "Chennai", "Kochi"]:
        weather = get_weather_data(city)
        if not weather:
            print(f"\nFailed to fetch data for {city}")
            continue
        
        alert = generate_alert(weather)
        print(f"\n{city} (Level: {alert['level'].value}):")
        
        for lang in ["en", "hi", "mr"]:
            print(f"\n[{lang.upper()}]")
            print(generate_nlp_message(weather, alert["level"], lang))
            print(f"\nSMS: {generate_sms_alert(weather, alert['level'], lang)}")

