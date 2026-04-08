from flask import Flask, jsonify, request, render_template_string
from weather_api import get_weather_data
from alert_engine import generate_alert, format_alert_for_display, AlertLevel
from nlp_generator import generate_nlp_message, generate_sms_alert, generate_voice_text
from document_extractor import DocumentExtractor, extract_from_text

app = Flask(__name__)


# Main HTML template with full UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fishermen Alert System</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }
        
        /* Navigation */
        .navbar {
            background: rgba(0,0,0,0.3);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: #0ea5e9;
        }
        
        .nav-links {
            display: flex;
            gap: 20px;
        }
        
        .nav-links a {
            color: #fff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            transition: background 0.3s;
        }
        
        .nav-links a:hover, .nav-links a.active {
            background: rgba(14, 165, 233, 0.3);
        }
        
        /* Main Container */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        /* Page Title */
        .page-title {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .page-title h1 {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .page-title p {
            color: rgba(255,255,255,0.7);
        }
        
        /* Tabs */
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .tab-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .tab-btn:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .tab-btn.active {
            background: #0ea5e9;
        }
        
        /* Tab Content */
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* Cards */
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        
        .card h3 {
            margin-bottom: 15px;
            color: #0ea5e9;
        }
        
        /* Form Elements */
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        input[type="text"], select, textarea {
            width: 100%;
            padding: 12px 15px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            background: rgba(255,255,255,0.1);
            color: #fff;
        }
        
        input::placeholder, textarea::placeholder {
            color: rgba(255,255,255,0.5);
        }
        
        textarea {
            min-height: 200px;
            resize: vertical;
        }
        
        select {
            cursor: pointer;
        }
        
        select option {
            background: #1a1a2e;
            color: #fff;
        }
        
        /* Buttons */
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: #0ea5e9;
            color: #fff;
        }
        
        .btn-primary:hover {
            background: #0284c7;
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.2);
            color: #fff;
        }
        
        .btn-secondary:hover {
            background: rgba(255,255,255,0.3);
        }
        
        /* Alert Box */
        .alert-box {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
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
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        
        /* Weather Details Grid */
        .details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .detail-item {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .detail-label {
            font-size: 0.85rem;
            opacity: 0.7;
            margin-bottom: 5px;
        }
        
        .detail-value {
            font-size: 1.3rem;
            font-weight: bold;
        }
        
        /* Recommendation Box */
        .recommendation {
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            border-left: 3px solid #0ea5e9;
        }
        
        /* Extraction Results */
        .extraction-results {
            margin-top: 20px;
        }
        
        .category-section {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .category-title {
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 10px;
            color: #0ea5e9;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .category-items {
            list-style: none;
        }
        
        .category-items li {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            line-height: 1.5;
        }
        
        .category-items li:last-child {
            border-bottom: none;
        }
        
        /* Stats Box */
        .stats-box {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .stat-item {
            background: rgba(14, 165, 233, 0.2);
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #0ea5e9;
        }
        
        .stat-label {
            font-size: 0.85rem;
            opacity: 0.8;
        }
        
        /* Contacts List */
        .contacts-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .contact-badge {
            background: rgba(239, 68, 68, 0.3);
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 500;
        }
        
        /* Loading */
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top-color: #0ea5e9;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Scenario Buttons */
        .scenario-btns {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .scenario-btn {
            padding: 10px 20px;
            border: 2px solid transparent;
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: #fff;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .scenario-btn:hover {
            border-color: #0ea5e9;
        }
        
        .scenario-btn.active {
            background: #0ea5e9;
        }
        
        /* Language selector */
        .lang-btns {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .lang-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            background: rgba(255,255,255,0.1);
            color: #fff;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .lang-btn.active {
            background: #0ea5e9;
        }
        
        /* Mobile Responsive */
        @media (max-width: 600px) {
            .navbar {
                flex-direction: column;
                gap: 15px;
            }
            
            .nav-links {
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .details-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="logo">Fishermen Alert System</div>
        <div class="nav-links">
            <a href="#" onclick="showTab('weather')" id="nav-weather" class="active">Weather Alerts</a>
            <a href="#" onclick="showTab('extract')" id="nav-extract">Guidelines Extractor</a>
            <a href="#" onclick="showTab('about')" id="nav-about">About</a>
        </div>
    </nav>
    
    <div class="container">
        
        <!-- Weather Alert Tab -->
        <div id="tab-weather" class="tab-content active">
            <div class="page-title">
                <h1>Weather Alert System</h1>
                <p>Check weather conditions before going fishing</p>
            </div>
            
            <div class="card">
                <h3>Enter Location</h3>
                <div class="form-group">
                    <input type="text" id="location" placeholder="Enter city name (e.g., Mumbai, Chennai, Kochi)" value="Mumbai">
                </div>
                
                <div class="form-group">
                    <label>Select Language:</label>
                    <div class="lang-btns">
                        <button class="lang-btn active" onclick="setLang('en', this)">English</button>
                        <button class="lang-btn" onclick="setLang('hi', this)">Hindi</button>
                        <button class="lang-btn" onclick="setLang('mr', this)">Marathi</button>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Test Scenario (for demo):</label>
                    <div class="scenario-btns">
                        <button class="scenario-btn active" onclick="setScenario('normal', this)">Normal</button>
                        <button class="scenario-btn" onclick="setScenario('windy', this)">Windy</button>
                        <button class="scenario-btn" onclick="setScenario('heavy_rain', this)">Heavy Rain</button>
                        <button class="scenario-btn" onclick="setScenario('storm', this)">Storm</button>
                    </div>
                </div>
                
                <button class="btn btn-primary" onclick="getWeatherAlert()">
                    Check Weather
                </button>
            </div>
            
            <div id="weather-result"></div>
        </div>
        
        <!-- Guidelines Extractor Tab -->
        <div id="tab-extract" class="tab-content">
            <div class="page-title">
                <h1>Guidelines Extractor</h1>
                <p>Upload fishing guidelines to extract important information</p>
            </div>
            
            <div class="card">
                <h3>Enter Guidelines Text</h3>
                <div class="form-group">
                    <textarea id="guidelines-text" placeholder="Paste your fishing guidelines here...

Example:
FISHING SAFETY GUIDELINES

WARNING: Always check weather forecast before going to sea. Wind speeds above 40 km/h are dangerous for small boats.

EMERGENCY CONTACTS:
- Coast Guard: 1554
- Marine Police: 100

REGULATIONS:
- Fishing license required
- Minimum fish size: 25 cm
- Maximum catch: 50 kg per day"></textarea>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button class="btn btn-primary" onclick="extractGuidelines()">
                        Extract Information
                    </button>
                    <button class="btn btn-secondary" onclick="loadSampleText()">
                        Load Sample
                    </button>
                </div>
            </div>
            
            <div id="extract-result"></div>
        </div>
        
        <!-- About Tab -->
        <div id="tab-about" class="tab-content">
            <div class="page-title">
                <h1>About This System</h1>
                <p>Helping fishermen stay safe</p>
            </div>
            
            <div class="card">
                <h3>Fishermen Alert System v1.0</h3>
                <p style="line-height: 1.8; margin-bottom: 20px;">
                    A comprehensive safety system designed to help fishermen make informed decisions 
                    about when to go fishing based on weather conditions, and to quickly extract 
                    important information from fishing guidelines and regulations.
                </p>
                
                <h3 style="margin-top: 25px;">Features</h3>
                <ul style="line-height: 2; margin-left: 20px; margin-top: 10px;">
                    <li>Real-time weather-based safety alerts</li>
                    <li>Multi-language support (English, Hindi, Marathi)</li>
                    <li>SMS and voice-ready alert formats</li>
                    <li>Automatic extraction of safety information from documents</li>
                    <li>Emergency contact detection</li>
                    <li>Important numbers and limits extraction</li>
                </ul>
                
                <h3 style="margin-top: 25px;">Alert Levels</h3>
                <div class="details-grid" style="margin-top: 15px;">
                    <div class="detail-item" style="border-left: 4px solid #22c55e;">
                        <div class="detail-label">SAFE</div>
                        <div class="detail-value" style="color: #22c55e;">Good</div>
                        <small>Wind &lt; 20 km/h</small>
                    </div>
                    <div class="detail-item" style="border-left: 4px solid #f59e0b;">
                        <div class="detail-label">CAUTION</div>
                        <div class="detail-value" style="color: #f59e0b;">Be Careful</div>
                        <small>Wind 20-35 km/h</small>
                    </div>
                    <div class="detail-item" style="border-left: 4px solid #ef4444;">
                        <div class="detail-label">DANGEROUS</div>
                        <div class="detail-value" style="color: #ef4444;">Stay Home</div>
                        <small>Wind &gt; 35 km/h</small>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
    
    <script>
        let currentLang = 'en';
        let currentScenario = 'normal';
        
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active from nav
            document.querySelectorAll('.nav-links a').forEach(link => {
                link.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById('tab-' + tabName).classList.add('active');
            document.getElementById('nav-' + tabName).classList.add('active');
        }
        
        function setLang(lang, btn) {
            currentLang = lang;
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }
        
        function setScenario(scenario, btn) {
            currentScenario = scenario;
            document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }
        
        async function getWeatherAlert() {
            const location = document.getElementById('location').value || 'Mumbai';
            const container = document.getElementById('weather-result');
            
            container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Fetching weather data...</p></div>';
            
            try {
                const response = await fetch(`/api/alert?location=${encodeURIComponent(location)}&lang=${currentLang}&scenario=${currentScenario}`);
                const data = await response.json();
                
                const levelClass = data.level === 'safe' ? 'alert-safe' : 
                                   data.level === 'caution' ? 'alert-caution' : 'alert-dangerous';
                
                const levelColor = data.level === 'safe' ? '#22c55e' : 
                                   data.level === 'caution' ? '#f59e0b' : '#ef4444';
                
                container.innerHTML = `
                    <div class="alert-box ${levelClass}">
                        <div class="alert-header">
                            <span class="alert-icon">${data.icon}</span>
                            <span class="alert-title">${data.title}</span>
                        </div>
                        
                        <div class="alert-message">
                            ${data.nlp_message}
                        </div>
                        
                        <div class="details-grid">
                            <div class="detail-item">
                                <div class="detail-label">Wind Speed</div>
                                <div class="detail-value">${data.details.wind_speed.toFixed(0)} km/h</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Temperature</div>
                                <div class="detail-value">${data.details.temperature.toFixed(0)}°C</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Visibility</div>
                                <div class="detail-value">${data.details.visibility.toFixed(0)} km</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Rainfall</div>
                                <div class="detail-value">${data.details.rain_1h.toFixed(1)} mm/h</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Wave Height</div>
                                <div class="detail-value">${(data.details.wave_height || 0).toFixed(2)} m</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Swell</div>
                                <div class="detail-value">${(data.details.swell_wave_height || 0).toFixed(2)} m</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Wave Period</div>
                                <div class="detail-value">${(data.details.wave_period || 0).toFixed(1)} s</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Ocean Current</div>
                                <div class="detail-value">${(data.details.ocean_current_velocity || 0).toFixed(2)} km/h</div>
                            </div>
                        </div>
                        
                        <div class="recommendation">
                            <strong>Recommendation:</strong> ${data.recommendation}
                        </div>
                        
                        <div style="margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 10px;">
                            <strong>SMS Alert:</strong><br>
                            <code style="color: #0ea5e9;">${data.sms_message}</code>
                        </div>
                    </div>
                `;
            } catch (error) {
                container.innerHTML = `<div class="alert-box alert-caution">
                    <p style="color: #ef4444;">Error: ${error.message}</p>
                </div>`;
            }
        }
        
        function loadSampleText() {
            document.getElementById('guidelines-text').value = `FISHING SAFETY GUIDELINES FOR COASTAL FISHERMEN

WARNING: Always check weather forecast before going to sea. Wind speeds above 40 km/h are extremely dangerous for small boats. Never go fishing alone during rough weather.

SAFETY EQUIPMENT REQUIRED:
- Life jacket must be worn at all times while on boat
- Carry a well-stocked first aid kit
- GPS device is strongly recommended for navigation
- Minimum boat length should be 15 feet for offshore fishing
- Working radio/communication device mandatory

EMERGENCY CONTACTS:
- Coast Guard Helpline: 1554
- Marine Police: 100
- Emergency Medical: 108
- Fisheries Department: 1800-123-4567
- District Control Room: 0484-2394567

FISHING REGULATIONS:
- Valid fishing license required (Fine: Rs.5000 for violation)
- Minimum catch size: 25 cm for most species
- Fishing prohibited during monsoon season (June 15 - August 15)
- Maximum catch limit: 50 kg per day per boat
- Protected species must not be caught - penalty up to Rs.50,000

WEATHER WARNING SIGNALS:
- Red flag hoisted: Do not venture into sea under any circumstances
- Yellow flag: Exercise extreme caution, stay near shore
- Green flag: Conditions safe for fishing
- Two red flags: Cyclone warning, return immediately

IMPORTANT DISTANCES:
- Stay within 12 km of shore if weather uncertain
- Maintain 500 meter distance from other fishing boats
- Do not fish within 3 km of port/harbor areas`;
        }
        
        async function extractGuidelines() {
            const text = document.getElementById('guidelines-text').value;
            const container = document.getElementById('extract-result');
            
            if (!text.trim()) {
                container.innerHTML = '<div class="alert-box alert-caution"><p>Please enter some text to analyze.</p></div>';
                return;
            }
            
            container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Analyzing document...</p></div>';
            
            try {
                const response = await fetch('/api/extract', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                const data = await response.json();
                
                let html = '<div class="extraction-results">';
                
                // Statistics
                html += `
                    <div class="stats-box">
                        <div class="stat-item">
                            <div class="stat-value">${data.statistics.total_words}</div>
                            <div class="stat-label">Words</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${data.statistics.total_sentences}</div>
                            <div class="stat-label">Sentences</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${data.statistics.categories_found.length}</div>
                            <div class="stat-label">Categories</div>
                        </div>
                    </div>
                `;
                
                // Emergency Contacts
                if (data.emergency_contacts && data.emergency_contacts.length > 0) {
                    html += `
                        <div class="category-section" style="border-left: 4px solid #ef4444;">
                            <div class="category-title">EMERGENCY CONTACTS</div>
                            <div class="contacts-list">
                                ${[...new Set(data.emergency_contacts.map(c => c.number))].map(num => 
                                    `<span class="contact-badge">${num}</span>`
                                ).join('')}
                            </div>
                        </div>
                    `;
                }
                
                // Key Points by Category
                const categoryIcons = {
                    'safety': 'SAFETY',
                    'weather': 'WEATHER',
                    'regulations': 'REGULATIONS',
                    'equipment': 'EQUIPMENT',
                    'emergency': 'EMERGENCY',
                    'general': 'GENERAL'
                };
                
                const categoryColors = {
                    'safety': '#22c55e',
                    'weather': '#0ea5e9',
                    'regulations': '#f59e0b',
                    'equipment': '#8b5cf6',
                    'emergency': '#ef4444',
                    'general': '#6b7280'
                };
                
                for (const [category, points] of Object.entries(data.key_points)) {
                    if (points.length > 0) {
                        html += `
                            <div class="category-section" style="border-left: 4px solid ${categoryColors[category] || '#6b7280'};">
                                <div class="category-title">${categoryIcons[category] || category.toUpperCase()}</div>
                                <ul class="category-items">
                                    ${points.slice(0, 5).map(point => 
                                        `<li>${point.length > 150 ? point.substring(0, 150) + '...' : point}</li>`
                                    ).join('')}
                                </ul>
                            </div>
                        `;
                    }
                }
                
                // Important Numbers
                if (data.important_numbers && data.important_numbers.length > 0) {
                    html += `
                        <div class="category-section" style="border-left: 4px solid #8b5cf6;">
                            <div class="category-title">IMPORTANT NUMBERS & LIMITS</div>
                            <ul class="category-items">
                                ${[...new Map(data.important_numbers.map(n => [n.value, n])).values()].slice(0, 8).map(num => 
                                    `<li><strong>${num.value}</strong> <small style="opacity:0.7">(${num.type})</small></li>`
                                ).join('')}
                            </ul>
                        </div>
                    `;
                }
                
                html += '</div>';
                container.innerHTML = html;
                
            } catch (error) {
                container.innerHTML = `<div class="alert-box alert-caution">
                    <p style="color: #ef4444;">Error: ${error.message}</p>
                </div>`;
            }
        }
        
        // Load initial weather alert
        getWeatherAlert();
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
    """
    location = request.args.get("location", "Mumbai")
    language = request.args.get("lang", "en")
    
    # Get real weather + ocean data
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


@app.route("/api/extract", methods=["POST"])
def extract_guidelines():
    """
    Extract information from guidelines text.
    """
    data = request.get_json()
    text = data.get("text", "")
    
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400
    
    # Extract information
    extractor = DocumentExtractor()
    summary = extractor.generate_summary(text)
    
    return jsonify(summary)


@app.route("/api/sms")
def get_sms_alert():
    """Get a short SMS-friendly alert."""
    location = request.args.get("location", "Mumbai")
    language = request.args.get("lang", "en")
    
    weather_data = get_weather_data(location)
    
    alert = generate_alert(weather_data)
    sms = generate_sms_alert(weather_data, alert["level"], language)
    
    return sms, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/api/voice")
def get_voice_alert():
    """Get text optimized for text-to-speech."""
    location = request.args.get("location", "Mumbai")
    language = request.args.get("lang", "en")
    
    weather_data = get_weather_data(location)
    
    alert = generate_alert(weather_data)
    voice = generate_voice_text(weather_data, alert["level"], language)
    
    return voice, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/api/health")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "fishermen-alert-system"})


if __name__ == "__main__":
    print("\nFISHERMEN ALERT SYSTEM - Web Server\n")
    print("  Web interface: http://localhost:5000")
    print("  API endpoint:  http://localhost:5000/api/alert")
    print("\n  Press Ctrl+C to stop the server.\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
