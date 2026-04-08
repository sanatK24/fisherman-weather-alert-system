# 🎣 Fishermen Alert System

A comprehensive safety system for fishermen with weather-based alerts and guidelines document extraction using NLP.

## Features

### 🌦️ Weather Alert System
- **Real-time weather integration**: Fetches data from OpenWeatherMap API
- **Rule-based alert engine**: Analyzes wind speed, visibility, rainfall, and conditions
- **Multi-language support**: English, Hindi (हिंदी), and Marathi (मराठी)
- **Multiple output formats**: Full alerts, SMS-friendly, voice-optimized

### 📄 Guidelines Extractor (NEW)
- **Document analysis**: Upload fishing guidelines and extract key information
- **Category detection**: Automatically categorizes into Safety, Weather, Regulations, Equipment, Emergency
- **Contact extraction**: Finds emergency numbers and helplines automatically
- **Important numbers**: Extracts limits, distances, fines, and other numerical data

## Alert Levels

| Level | Icon | Condition |
|-------|------|-----------|
| ✅ Safe | Green | Wind < 20 km/h, good visibility, no rain |
| ⚠️ Caution | Yellow | Wind 20-35 km/h, moderate visibility, light rain |
| 🚫 Dangerous | Red | Wind > 35 km/h, poor visibility, heavy rain/storm |

## Quick Start

### 1. Installation

```bash
# Navigate to project
cd mini-project

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

**Interactive Menu Mode (Recommended):**
```bash
python main.py
```

This opens an interactive menu with options:
1. 🌦️ Weather Alert System
2. 📄 Guidelines Extractor
3. 🎬 Run Demo
4. ℹ️ About
5. 🚪 Exit

**Command Line Options:**
```bash
# Weather alerts
python main.py -l Mumbai                    # Check weather for Mumbai
python main.py -l Chennai --lang hi         # Hindi alert
python main.py -l Kochi --format sms        # SMS format
python main.py -l Goa --scenario storm      # Test storm scenario

# Document extraction
python main.py --extract guidelines.txt     # Extract from file

# Demo
python main.py --demo                       # Run demonstration
```

**Web Interface:**
```bash
python app.py
# Open http://localhost:5000 in browser
```

## Menu Structure

```
MAIN MENU
├── 1. Weather Alert System
│   ├── Check Weather by Location
│   ├── Multi-language Alert
│   ├── SMS Format Alert
│   ├── Voice Alert Text
│   └── Test Scenarios
│
├── 2. Guidelines Extractor
│   ├── Upload Document File
│   ├── Enter Text Manually
│   └── View Sample Analysis
│
├── 3. Run Demo
├── 4. About
└── 5. Exit
```

## Guidelines Extractor Example

**Input Document:**
```
FISHING SAFETY GUIDELINES
WARNING: Wind above 40 km/h is dangerous.
Emergency Contact: Coast Guard 1554
Minimum fish size: 25 cm
Fine for violation: ₹5000
```

**Extracted Output:**
```
📄 DOCUMENT ANALYSIS SUMMARY
════════════════════════════════════════════════════

📊 Statistics:
   • Total words: 24
   • Categories found: safety, regulations, emergency

📋 KEY POINTS BY CATEGORY

🛡️ SAFETY:
   1. WARNING: Wind above 40 km/h is dangerous.

📜 REGULATIONS:
   1. Minimum fish size: 25 cm
   2. Fine for violation: ₹5000

📞 EMERGENCY CONTACTS FOUND
   • 1554: Coast Guard

🔢 IMPORTANT NUMBERS/LIMITS
   • 40 km/h (speed)
   • 25 cm (size)
   • ₹5000 (amount)
```

## Project Structure

```
mini-project/
├── weather_api.py        # Weather data fetching
├── alert_engine.py       # Rule-based alert logic
├── nlp_generator.py      # Natural language generation
├── document_extractor.py # Guidelines extraction (NEW)
├── app.py                # Flask web application
├── main.py               # CLI with interactive menu
├── test_system.py        # Test suite
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Web interface |
| `GET /api/alert?location=Mumbai&lang=en` | Full alert JSON |
| `GET /api/sms?location=Mumbai&lang=hi` | SMS-friendly text |
| `GET /api/voice?location=Mumbai` | TTS-optimized text |
| `GET /api/health` | Health check |

## Testing

```bash
# Run all tests
python test_system.py

# Or with pytest
pytest test_system.py -v
```

## Future Improvements

- [ ] PDF document support
- [ ] Machine Learning for better predictions
- [ ] GPS-based automatic location
- [ ] Push notifications
- [ ] Voice alerts with Text-to-Speech
- [ ] WhatsApp/Telegram bot integration

## License

MIT License - Feel free to use and modify for your needs.
