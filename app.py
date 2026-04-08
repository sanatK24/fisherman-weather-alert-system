"""
Flask API for Fishermen Alert System
Provides REST endpoints for weather alerts
"""

from flask import Flask, jsonify, request, render_template_string
from weather_api import get_weather_data, get_mock_weather_data
from alert_engine import generate_alert, format_alert_for_display, AlertLevel
from nlp_generator import generate_nlp_message, generate_sms_alert, generate_voice_text

app = Flask(__name__)

# Configuration
USE_MOCK_DATA = True  # Set to False when you have a real API key


# HTML template for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎣 Fishermen Alert System</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 30px; font-size: 2rem; }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            background: rgba(255,255,255,0.1);
            color: #fff;
        }
        input::placeholder { color: rgba(255,255,255,0.5); }
        button {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            background: #0ea5e9;
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover { background: #0284c7; }
        .alert-box {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .alert-safe { border-left: 5px solid #22c55e; }
        .alert-caution { border-left: 5px solid #f59e0b; }
        .alert-dangerous { border-left: 5px solid #ef4444; }
        .alert-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .alert-icon { font-size: 2.5rem; }
        .alert-title { font-size: 1.3rem; font-weight: bold; }
        .alert-message { 
            font-size: 1.1rem; 
            line-height: 1.6;
            margin-bottom: 20px;
        }
        .details { 
            display: grid; 
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .detail-item {
            background: rgba(0,0,0,0.2);
            padding: 10px;
            border-radius: 8px;
        }
        .detail-label { font-size: 0.8rem; opacity: 0.7; }
        .detail-value { font-size: 1.2rem; font-weight: bold; }
        .recommendation {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        .language-select {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
        }
        .lang-btn {
            padding: 8px 16px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 5px;
            color: #fff;
            cursor: pointer;
        }
        .lang-btn.active { background: #0ea5e9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎣 Fishermen Alert System</h1>
        
        <div class="search-box">
            <input type="text" id="location" placeholder="Enter city name (e.g., Mumbai)" value="Mumbai">
            <button onclick="getAlert()">Check Weather</button>
        </div>
        
        <div class="language-select">
            <button class="lang-btn active" onclick="setLang('en')">English</button>
            <button class="lang-btn" onclick="setLang('hi')">हिंदी</button>
            <button class="lang-btn" onclick="setLang('mr')">मराठी</button>
        </div>
        
        <div id="alert-container"></div>
    </div>
    
    <script>
        let currentLang = 'en';
        
        function setLang(lang) {
            currentLang = lang;
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            getAlert();
        }
        
        async function getAlert() {
            const location = document.getElementById('location').value || 'Mumbai';
            const container = document.getElementById('alert-container');
            container.innerHTML = '<p style="text-align:center">Loading...</p>';
            
            try {
                const response = await fetch(`/api/alert?location=${encodeURIComponent(location)}&lang=${currentLang}`);
                const data = await response.json();
                
                const levelClass = data.level === 'safe' ? 'alert-safe' : 
                                   data.level === 'caution' ? 'alert-caution' : 'alert-dangerous';
                
                container.innerHTML = `
                    <div class="alert-box ${levelClass}">
                        <div class="alert-header">
                            <span class="alert-icon">${data.icon}</span>
                            <span class="alert-title">${data.title}</span>
                        </div>
                        <p class="alert-message">${data.nlp_message}</p>
                        <div class="details">
                            <div class="detail-item">
                                <div class="detail-label">💨 Wind Speed</div>
                                <div class="detail-value">${data.details.wind_speed.toFixed(1)} km/h</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">🌡️ Temperature</div>
                                <div class="detail-value">${data.details.temperature.toFixed(1)}°C</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">👁️ Visibility</div>
                                <div class="detail-value">${data.details.visibility.toFixed(1)} km</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">🌧️ Rain</div>
                                <div class="detail-value">${data.details.rain_1h.toFixed(1)} mm/h</div>
                            </div>
                        </div>
                        <div class="recommendation">
                            <strong>💡 Recommendation:</strong> ${data.recommendation}
                        </div>
                    </div>
                `;
            } catch (error) {
                container.innerHTML = `<p style="color: #ef4444; text-align: center;">Error: ${error.message}</p>`;
            }
        }
        
        // Load initial alert
        getAlert();
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    """Serve the web interface."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/alert")
def get_alert():
    """
    Get fishing safety alert for a location.
    
    Query params:
        location: City name (default: Mumbai)
        lang: Language code - en, hi, mr (default: en)
        mock: Use mock data - true/false (default: based on USE_MOCK_DATA)
        scenario: Mock scenario - normal, windy, storm, heavy_rain (default: normal)
    
    Returns:
        JSON alert data
    """
    location = request.args.get("location", "Mumbai")
    language = request.args.get("lang", "en")
    use_mock = request.args.get("mock", str(USE_MOCK_DATA)).lower() == "true"
    scenario = request.args.get("scenario", "normal")
    
    # Get weather data
    if use_mock:
        weather_data = get_mock_weather_data(location, scenario)
    else:
        weather_data = get_weather_data(location)
    
    # Generate alert
    alert = generate_alert(weather_data)
    
    # Generate NLP message in requested language
    nlp_message = generate_nlp_message(weather_data, alert["level"], language)
    sms_message = generate_sms_alert(weather_data, alert["level"], language)
    voice_text = generate_voice_text(weather_data, alert["level"], language)
    
    return jsonify({
        "level": alert["level"].value,
        "icon": alert["icon"],
        "title": alert["title"],
        "message": alert["message"],
        "nlp_message": nlp_message,
        "sms_message": sms_message,
        "voice_text": voice_text,
        "reasons": alert["reasons"],
        "recommendation": alert["recommendation"],
        "location": alert["location"],
        "details": alert["details"],
        "language": language
    })


@app.route("/api/sms")
def get_sms_alert():
    """
    Get a short SMS-friendly alert.
    
    Query params:
        location: City name
        lang: Language code
    
    Returns:
        Short text message suitable for SMS
    """
    location = request.args.get("location", "Mumbai")
    language = request.args.get("lang", "en")
    
    if USE_MOCK_DATA:
        weather_data = get_mock_weather_data(location)
    else:
        weather_data = get_weather_data(location)
    
    alert = generate_alert(weather_data)
    sms = generate_sms_alert(weather_data, alert["level"], language)
    
    return sms, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/api/voice")
def get_voice_alert():
    """
    Get text optimized for text-to-speech.
    
    Query params:
        location: City name
        lang: Language code
    
    Returns:
        Text suitable for TTS conversion
    """
    location = request.args.get("location", "Mumbai")
    language = request.args.get("lang", "en")
    
    if USE_MOCK_DATA:
        weather_data = get_mock_weather_data(location)
    else:
        weather_data = get_weather_data(location)
    
    alert = generate_alert(weather_data)
    voice = generate_voice_text(weather_data, alert["level"], language)
    
    return voice, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/api/health")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "fishermen-alert-system"})


if __name__ == "__main__":
    print("🎣 Starting Fishermen Alert System...")
    print("📍 Web interface: http://localhost:5000")
    print("📡 API endpoint: http://localhost:5000/api/alert?location=Mumbai")
    print("📱 SMS endpoint: http://localhost:5000/api/sms?location=Mumbai")
    print("\nPress Ctrl+C to stop the server.")
    app.run(debug=True, host="0.0.0.0", port=5000)
