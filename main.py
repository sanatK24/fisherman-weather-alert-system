"""
Fishermen Alert System - Main CLI Application
Combines all modules for command-line usage with interactive menu
"""

import argparse
import sys
import os
from weather_api import get_weather_data, get_mock_weather_data
from alert_engine import generate_alert, format_alert_for_display, AlertLevel
from nlp_generator import generate_nlp_message, generate_sms_alert, generate_voice_text
from document_extractor import DocumentExtractor, extract_from_file, extract_from_text


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Print the application banner."""
    banner = """
============================================================
          FISHERMEN ALERT SYSTEM                
      Weather-based Safety Alerts for Fishermen         
============================================================
    """
    print(banner)


def print_main_menu():
    """Print the main menu options."""
    menu = """
------------------------------------------------------------
                      MAIN MENU                            
------------------------------------------------------------

   1. Weather Alert System                             
      Check current weather conditions for fishing         

   2. Guidelines Extractor                             
      Upload & extract important info from documents       

   3. Run Demo                                         
      See demonstration of all features                    

   4. About                                            
      Learn about this system                              

   5. Exit                                              
      Close the application                                

------------------------------------------------------------
    """
    print(menu)


def print_weather_menu():
    """Print weather alert submenu."""
    menu = """
------------------------------------------------------------
              WEATHER ALERT SYSTEM                     
------------------------------------------------------------

   1. Check Weather by Location                        
      Enter city name to get fishing safety alert          

   2. Multi-language Alert                             
      Get alerts in Hindi/Marathi/English                  

   3. SMS Format Alert                                 
      Get short SMS-friendly alert                         

   4. Voice Alert Text                                 
      Get text optimized for voice/TTS                     

   5. Test Scenarios                                   
      Test with different weather conditions               

   6. Back to Main Menu                                

------------------------------------------------------------
    """
    print(menu)


def print_guidelines_menu():
    """Print guidelines extractor submenu."""
    menu = """
------------------------------------------------------------
              GUIDELINES EXTRACTOR                     
------------------------------------------------------------

   1. Upload Document File                             
      Extract info from .txt file                          

   2. Enter Text Manually                              
      Paste or type guidelines text                        

   3. View Sample Analysis                             
      See example with sample guidelines                   

   4. Back to Main Menu                                

------------------------------------------------------------
    """
    print(menu)


def run_interactive_mode():
    """Run the system in interactive mode with main menu."""
    while True:
        clear_screen()
        print_banner()
        print_main_menu()
        
        choice = input("   Enter your choice (1-5): ").strip()
        
        if choice == "1":
            weather_menu_loop()
        elif choice == "2":
            guidelines_menu_loop()
        elif choice == "3":
            run_demo()
            input("\nPress Enter to return to main menu...")
        elif choice == "4":
            show_about()
            input("\nPress Enter to return to main menu...")
        elif choice == "5":
            clear_screen()
            print("\n👋 Thank you for using Fishermen Alert System!")
            print("   Stay safe on the water! 🎣\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")
            input("Press Enter to continue...")


def weather_menu_loop():
    """Handle weather alert submenu."""
    while True:
        clear_screen()
        print_banner()
        print_weather_menu()
        
        choice = input("   Enter your choice (1-6): ").strip()
        
        if choice == "1":
            check_weather_by_location()
        elif choice == "2":
            check_weather_multilang()
        elif choice == "3":
            get_sms_alert()
        elif choice == "4":
            get_voice_alert()
        elif choice == "5":
            test_weather_scenarios()
        elif choice == "6":
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-6.")
            input("Press Enter to continue...")


def guidelines_menu_loop():
    """Handle guidelines extractor submenu."""
    while True:
        clear_screen()
        print_banner()
        print_guidelines_menu()
        
        choice = input("   Enter your choice (1-4): ").strip()
        
        if choice == "1":
            extract_from_document()
        elif choice == "2":
            extract_from_manual_text()
        elif choice == "3":
            show_sample_analysis()
        elif choice == "4":
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-4.")
            input("Press Enter to continue...")


def check_weather_by_location():
    """Check weather for a specific location."""
    print("\n" + "=" * 50)
    print("CHECK WEATHER BY LOCATION")
    print("=" * 50)
    
    location = input("\nEnter city name (e.g., Mumbai, Chennai): ").strip()
    if not location:
        location = "Mumbai"
        print(f"   Using default: {location}")
    
    print("\nFetching weather data...")
    
    # Use mock data for demo
    weather_data = get_mock_weather_data(location)
    
    if weather_data is None:
        print("ERROR: Failed to fetch weather data.")
        input("\nPress Enter to continue...")
        return
    
    alert = generate_alert(weather_data)
    print(format_alert_for_display(alert))
    
    # Show NLP message
    print(f"Natural Language Alert:")
    print("-" * 40)
    print(generate_nlp_message(weather_data, alert["level"], "en"))
    
    input("\nPress Enter to continue...")


def check_weather_multilang():
    """Check weather with language selection."""
    print("\n" + "=" * 50)
    print("MULTI-LANGUAGE WEATHER ALERT")
    print("=" * 50)
    
    location = input("\nEnter city name: ").strip() or "Mumbai"
    
    print("\nSelect language:")
    print("   1. English")
    print("   2. Hindi")
    print("   3. Marathi")
    
    lang_choice = input("\n   Choice [1]: ").strip() or "1"
    lang_map = {"1": "en", "2": "hi", "3": "mr"}
    language = lang_map.get(lang_choice, "en")
    
    weather_data = get_mock_weather_data(location)
    alert = generate_alert(weather_data)
    
    print("\n" + "=" * 50)
    print(f"{alert['icon']} {alert['title']}")
    print("=" * 50)
    print(f"\nLocation: {location}")
    print(f"Wind: {weather_data['wind_speed']:.0f} km/h")
    print(f"Temperature: {weather_data['temperature']:.0f} C")
    
    print(f"\nMessage ({language.upper()}):")
    print("-" * 40)
    print(generate_nlp_message(weather_data, alert["level"], language))
    
    input("\nPress Enter to continue...")


def get_sms_alert():
    """Get SMS-friendly short alert."""
    print("\n" + "=" * 50)
    print("📱 SMS FORMAT ALERT")
    print("=" * 50)
    
    location = input("\n📍 Enter city name: ").strip() or "Mumbai"
    
    print("\n🌐 Select language:")
    print("   1. English  2. Hindi  3. Marathi")
    lang_choice = input("   Choice [1]: ").strip() or "1"
    lang_map = {"1": "en", "2": "hi", "3": "mr"}
    language = lang_map.get(lang_choice, "en")
    
    weather_data = get_mock_weather_data(location)
    alert = generate_alert(weather_data)
    
    sms = generate_sms_alert(weather_data, alert["level"], language)
    
    print("\n" + "-" * 50)
    print("📱 SMS Alert (copy this):")
    print("-" * 50)
    print(f"\n{sms}\n")
    print("-" * 50)
    print(f"Characters: {len(sms)}")
    
    input("\nPress Enter to continue...")


def get_voice_alert():
    """Get voice/TTS optimized alert."""
    print("\n" + "=" * 50)
    print("🔊 VOICE ALERT TEXT")
    print("=" * 50)
    
    location = input("\n📍 Enter city name: ").strip() or "Mumbai"
    
    print("\n🌐 Select language:")
    print("   1. English  2. Hindi")
    lang_choice = input("   Choice [1]: ").strip() or "1"
    language = "hi" if lang_choice == "2" else "en"
    
    weather_data = get_mock_weather_data(location)
    alert = generate_alert(weather_data)
    
    voice = generate_voice_text(weather_data, alert["level"], language)
    
    print("\n" + "-" * 50)
    print("🔊 Voice Alert Text (for TTS):")
    print("-" * 50)
    print(f"\n{voice}\n")
    
    input("\nPress Enter to continue...")


def test_weather_scenarios():
    """Test different weather scenarios."""
    print("\n" + "=" * 50)
    print("🧪 TEST WEATHER SCENARIOS")
    print("=" * 50)
    
    print("\nSelect scenario:")
    print("   1. ✅ Normal (Safe)")
    print("   2. ⚠️ Windy (Caution)")
    print("   3. 🚫 Storm (Dangerous)")
    print("   4. 🌧️ Heavy Rain (Dangerous)")
    
    choice = input("\n   Choice [1]: ").strip() or "1"
    scenario_map = {"1": "normal", "2": "windy", "3": "storm", "4": "heavy_rain"}
    scenario = scenario_map.get(choice, "normal")
    
    location = input("\n📍 Enter city name [Mumbai]: ").strip() or "Mumbai"
    
    weather_data = get_mock_weather_data(location, scenario)
    alert = generate_alert(weather_data)
    
    print(format_alert_for_display(alert))
    print(f"📝 {generate_nlp_message(weather_data, alert['level'], 'en')}")
    
    input("\nPress Enter to continue...")


def extract_from_document():
    """Extract information from a document file."""
    print("\n" + "=" * 50)
    print("📁 EXTRACT FROM DOCUMENT FILE")
    print("=" * 50)
    
    print("\nSupported formats: .txt")
    filepath = input("\n📂 Enter file path: ").strip()
    
    if not filepath:
        print("❌ No file path provided.")
        input("\nPress Enter to continue...")
        return
    
    # Remove quotes if present
    filepath = filepath.strip('"\'')
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        input("\nPress Enter to continue...")
        return
    
    print("\n⏳ Analyzing document...")
    
    summary = extract_from_file(filepath)
    
    if summary is None:
        print("❌ Failed to extract information from file.")
        input("\nPress Enter to continue...")
        return
    
    extractor = DocumentExtractor()
    print(extractor.format_summary_for_display(summary))
    
    # Option to save
    save = input("\n💾 Save summary to file? (y/n): ").strip().lower()
    if save == 'y':
        output_file = filepath.rsplit('.', 1)[0] + "_summary.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extractor.format_summary_for_display(summary))
        print(f"✅ Summary saved to: {output_file}")
    
    input("\nPress Enter to continue...")


def extract_from_manual_text():
    """Extract information from manually entered text."""
    print("\n" + "=" * 50)
    print("✏️ ENTER TEXT MANUALLY")
    print("=" * 50)
    
    print("\nPaste or type your guidelines text below.")
    print("When done, type 'DONE' on a new line and press Enter.")
    print("-" * 50)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            lines.append(line)
        except EOFError:
            break
    
    text = '\n'.join(lines)
    
    if not text.strip():
        print("❌ No text provided.")
        input("\nPress Enter to continue...")
        return
    
    print("\n⏳ Analyzing text...")
    
    summary = extract_from_text(text)
    extractor = DocumentExtractor()
    print(extractor.format_summary_for_display(summary))
    
    input("\nPress Enter to continue...")


def show_sample_analysis():
    """Show sample analysis with demo text."""
    print("\n" + "=" * 50)
    print("📋 SAMPLE ANALYSIS")
    print("=" * 50)
    
    sample_text = """
    FISHING SAFETY GUIDELINES FOR COASTAL FISHERMEN
    
    WARNING: Always check weather forecast before going to sea. Wind speeds above 40 km/h 
    are extremely dangerous for small boats. Never go fishing alone during rough weather.
    
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
    - Valid fishing license required (Fine: ₹5000 for violation)
    - Minimum catch size: 25 cm for most species
    - Fishing prohibited during monsoon season (June 15 - August 15)
    - Maximum catch limit: 50 kg per day per boat
    - Protected species must not be caught - penalty up to ₹50,000
    
    WEATHER WARNING SIGNALS:
    - Red flag hoisted: Do not venture into sea under any circumstances
    - Yellow flag: Exercise extreme caution, stay near shore
    - Green flag: Conditions safe for fishing
    - Two red flags: Cyclone warning, return immediately
    
    IMPORTANT DISTANCES:
    - Stay within 12 km of shore if weather uncertain
    - Maintain 500 meter distance from other fishing boats
    - Do not fish within 3 km of port/harbor areas
    
    खतरा: तूफान के दौरान समुद्र में कभी न जाएं।
    सावधान: जीवन रक्षक जैकेट हमेशा पहनें।
    धोका: वादळी हवामानात समुद्रात जाऊ नका।
    """
    
    print("\n📄 Sample Guidelines Text:")
    print("-" * 50)
    print(sample_text[:500] + "...\n")
    
    print("⏳ Analyzing sample document...")
    
    summary = extract_from_text(sample_text)
    extractor = DocumentExtractor()
    print(extractor.format_summary_for_display(summary))
    
    input("\nPress Enter to continue...")


def show_about():
    """Show about information."""
    about = """
============================================================
                       ABOUT                               
============================================================

  FISHERMEN ALERT SYSTEM v1.0                          

  A comprehensive safety system for fishermen that:        

  * Provides real-time weather-based safety alerts        
  * Supports multiple languages (EN, HI, MR)              
  * Generates SMS and voice-ready alerts                  
  * Extracts key information from guidelines              
  * Identifies emergency contacts automatically           

  ALERT LEVELS:                                            
    SAFE      - Good conditions for fishing                  
    CAUTION   - Be careful, stay near shore               
    DANGEROUS - Do not go to sea                        

  THRESHOLDS:                                              
    Wind Speed: <20 Safe | 20-35 Caution | >35 Danger     
    Visibility: >5km Safe | 2-5km Caution | <2km Danger   
    Rainfall:   <2mm Safe | 2-10mm Caution | >10mm Danger   

============================================================
    """
    print(about)


def run_single_query(location: str, language: str = "en", use_mock: bool = True, 
                     scenario: str = "normal", output_format: str = "full"):
    """
    Run a single weather query and display the alert.
    
    Args:
        location: City name
        language: Language code (en, hi, mr)
        use_mock: Whether to use mock data
        scenario: Mock scenario type
        output_format: Output format (full, sms, json)
    """
    # Get weather data
    if use_mock:
        weather_data = get_mock_weather_data(location, scenario)
    else:
        weather_data = get_weather_data(location)
    
    if weather_data is None:
        print("Error: Could not fetch weather data", file=sys.stderr)
        sys.exit(1)
    
    # Generate alert
    alert = generate_alert(weather_data)
    
    # Output based on format
    if output_format == "sms":
        print(generate_sms_alert(weather_data, alert["level"], language))
    elif output_format == "voice":
        print(generate_voice_text(weather_data, alert["level"], language))
    elif output_format == "json":
        import json
        output = {
            "location": alert["location"],
            "level": alert["level"].value,
            "icon": alert["icon"],
            "title": alert["title"],
            "message": generate_nlp_message(weather_data, alert["level"], language),
            "recommendation": alert["recommendation"],
            "details": alert["details"]
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:  # full
        print_banner()
        print(format_alert_for_display(alert))
        print(f"📝 Message ({language.upper()}):")
        print(generate_nlp_message(weather_data, alert["level"], language))


def run_demo():
    """Run a demonstration of all scenarios."""
    clear_screen()
    print_banner()
    print("\n🎬 DEMONSTRATION MODE")
    print("=" * 60)
    print("Showing alerts for different weather scenarios\n")
    
    scenarios = [
        ("Mumbai", "normal", "Normal Conditions"),
        ("Chennai", "windy", "Windy Conditions"),
        ("Kochi", "heavy_rain", "Heavy Rain"),
        ("Goa", "storm", "Storm Warning")
    ]
    
    for location, scenario, description in scenarios:
        print(f"\n{'='*60}")
        print(f"📋 Scenario: {description}")
        print(f"{'='*60}")
        
        weather_data = get_mock_weather_data(location, scenario)
        alert = generate_alert(weather_data)
        
        print(f"\n{alert['icon']} {alert['title']}")
        print(f"📍 Location: {location}")
        print(f"💨 Wind: {weather_data['wind_speed']:.0f} km/h")
        print(f"🌡️ Temp: {weather_data['temperature']:.0f}°C")
        print(f"🌧️ Rain: {weather_data['rain_1h']:.0f} mm/h")
        print(f"\n📝 {generate_nlp_message(weather_data, alert['level'], 'en')}")
        
        input("\nPress Enter for next scenario...")
    
    # Demo document extraction
    print(f"\n{'='*60}")
    print("📄 DOCUMENT EXTRACTION DEMO")
    print(f"{'='*60}")
    
    sample = "WARNING: Wind above 40 km/h is dangerous. Emergency: Call 1554. Life jacket required."
    summary = extract_from_text(sample)
    
    print(f"\nSample text: \"{sample}\"")
    print(f"\nCategories found: {', '.join(summary['statistics']['categories_found'])}")
    print(f"Emergency contacts: {[c['number'] for c in summary['emergency_contacts']]}")
    
    print("\n✅ Demo complete!")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="🎣 Fishermen Alert System - Weather alerts & Guidelines extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Interactive menu mode
  python main.py -l Mumbai                # Weather alert for Mumbai
  python main.py -l Chennai --lang hi     # Hindi alert for Chennai
  python main.py --demo                   # Run demonstration
  python main.py -l Kochi --format sms    # SMS format output
  python main.py -l Goa --scenario storm  # Simulate storm scenario
  python main.py --extract guidelines.txt # Extract from document
        """
    )
    
    parser.add_argument("-l", "--location", type=str, help="City name to check weather")
    parser.add_argument("--lang", type=str, default="en", 
                        choices=["en", "hi", "mr"],
                        help="Language: en (English), hi (Hindi), mr (Marathi)")
    parser.add_argument("--format", type=str, default="full",
                        choices=["full", "sms", "voice", "json"],
                        help="Output format")
    parser.add_argument("--scenario", type=str, default="normal",
                        choices=["normal", "windy", "storm", "heavy_rain"],
                        help="Mock weather scenario (for testing)")
    parser.add_argument("--real-api", action="store_true",
                        help="Use real API instead of mock data")
    parser.add_argument("--demo", action="store_true",
                        help="Run demonstration mode")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Run in interactive menu mode")
    parser.add_argument("--extract", type=str, metavar="FILE",
                        help="Extract information from guidelines document")
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
        input("\nPress Enter to exit...")
    elif args.extract:
        # Extract from document
        filepath = args.extract
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        
        summary = extract_from_file(filepath)
        if summary is None:
            print("Error: Failed to extract information", file=sys.stderr)
            sys.exit(1)
        
        extractor = DocumentExtractor()
        print(extractor.format_summary_for_display(summary))
    elif args.location:
        run_single_query(
            location=args.location,
            language=args.lang,
            use_mock=not args.real_api,
            scenario=args.scenario,
            output_format=args.format
        )
    else:
        # Default to interactive menu mode
        run_interactive_mode()


if __name__ == "__main__":
    main()
