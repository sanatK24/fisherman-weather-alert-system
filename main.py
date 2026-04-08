import argparse
import sys
import os
from weather_api import get_weather_data
from alert_engine import generate_alert, format_alert_for_display, AlertLevel
from nlp_generator import generate_nlp_message, generate_sms_alert, generate_voice_text
from document_extractor import DocumentExtractor, extract_from_file, extract_from_text


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    print("\nFISHERMEN ALERT SYSTEM")
    print("   Weather-based Safety Alerts for Fishermen\n")


def print_main_menu():
    print("MAIN MENU\n")
    print("   1. Weather Alert System")
    print("   2. Guidelines Extractor")
    print("   3. Exit\n")


def print_weather_menu():
    print("\nWEATHER ALERT SYSTEM\n")
    print("   1. Check Weather by Location")
    print("   2. Back to Main Menu\n")


def print_guidelines_menu():
    print("\nGUIDELINES EXTRACTOR\n")
    print("   1. Upload Document File")
    print("   2. Enter Text Manually")
    print("   3. Back to Main Menu\n")


def run_interactive_mode():
    while True:
        clear_screen()
        print_banner()
        print_main_menu()
        
        choice = input("   Enter your choice (1-3): ").strip()
        
        if choice == "1":
            weather_menu_loop()
        elif choice == "2":
            guidelines_menu_loop()
        elif choice == "3":
            clear_screen()
            print("\n Thank you for using Fishermen Alert System!")
            print("   Stay safe on the water!\n")
            break
        else:
            print("\n Invalid choice. Please enter 1-3.")
            input("Press Enter to continue...")


def weather_menu_loop():
    while True:
        clear_screen()
        print_banner()
        print_weather_menu()
        
        choice = input("   Enter your choice (1-2): ").strip()
        
        if choice == "1":
            check_weather_by_location()
        elif choice == "2":
            break
        else:
            print("\n Invalid choice. Please enter 1-2.")
            input("Press Enter to continue...")


def guidelines_menu_loop():
    while True:
        clear_screen()
        print_banner()
        print_guidelines_menu()
        
        choice = input("   Enter your choice (1-3): ").strip()
        
        if choice == "1":
            extract_from_document()
        elif choice == "2":
            extract_from_manual_text()
        elif choice == "3":
            break
        else:
            print("\nInvalid choice. Please enter 1-3.")
            input("Press Enter to continue...")


def check_weather_by_location():
    print("\nCHECK WEATHER BY LOCATION\n")
    
    location = input("\nEnter city name (e.g., Mumbai, Chennai): ").strip()
    if not location:
        location = "Mumbai"
        print(f"   Using default: {location}")
    
    print("\nFetching real weather + ocean data...\n")
    
    weather_data = get_weather_data(location)
    
    if weather_data is None:
        print("ERROR: Failed to fetch weather data.")
        input("\nPress Enter to continue...")
        return
    
    alert = generate_alert(weather_data)
    print(format_alert_for_display(alert))
    
    print(f"\nNatural Language Alert:")
    print(generate_nlp_message(weather_data, alert["level"], "en"))
    
    print("\nLanguage options: (1) English  (2) Hindi  (3) Marathi")
    lang_choice = input("Language [1]: ").strip() or "1"
    lang_map = {"1": "en", "2": "hi", "3": "mr"}
    lang = lang_map.get(lang_choice, "en")
    
    if lang != "en":
        print(f"\nMessage ({lang.upper()}):")
        print(generate_nlp_message(weather_data, alert["level"], lang))
    
    input("\nPress Enter to continue...")


def extract_from_document():
    print("\nEXTRACT FROM DOCUMENT FILE\n")
    
    print("\nSupported formats: .txt")
    filepath = input("\nEnter file path: ").strip()
    
    if not filepath:
        print("No file path provided.")
        input("\nPress Enter to continue...")
        return
    
    filepath = filepath.strip('"\'')
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        input("\nPress Enter to continue...")
        return
    
    print("\nAnalyzing document...")
    
    summary = extract_from_file(filepath)
    
    if summary is None:
        print("Failed to extract information from file.")
        input("\nPress Enter to continue...")
        return
    
    extractor = DocumentExtractor()
    print(extractor.format_summary_for_display(summary))
    
    save = input("\nSave summary to file? (y/n): ").strip().lower()
    if save == 'y':
        output_file = filepath.rsplit('.', 1)[0] + "_summary.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extractor.format_summary_for_display(summary))
        print(f"Summary saved to: {output_file}")
    
    input("\nPress Enter to continue...")


def extract_from_manual_text():
    print("\nENTER TEXT MANUALLY\n")
    print("Paste or type your guidelines text below.")
    print("When done, type 'DONE' on a new line and press Enter.\n")
    
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
        print("No text provided.")
        input("\nPress Enter to continue...")
        return
    
    print("\nAnalyzing text...")
    
    summary = extract_from_text(text)
    extractor = DocumentExtractor()
    print(extractor.format_summary_for_display(summary))
    
    input("\nPress Enter to continue...")


def run_single_query(location: str, language: str = "en",
                     output_format: str = "full"):
    weather_data = get_weather_data(location)
    
    if weather_data is None:
        print("Error: Could not fetch weather data", file=sys.stderr)
        sys.exit(1)
    
    alert = generate_alert(weather_data)
    
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
    else:
        print_banner()
        print(format_alert_for_display(alert))
        print(f"Message ({language.upper()}):")
        print(generate_nlp_message(weather_data, alert["level"], language))


def main():
    parser = argparse.ArgumentParser(
        description="Fishermen Alert System - Weather alerts & Guidelines extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Interactive menu mode
  python main.py -l Mumbai                # Weather alert for Mumbai
  python main.py -l Chennai --lang hi     # Hindi alert for Chennai
  python main.py -l Kochi --format sms    # SMS format output
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
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Run in interactive menu mode")
    parser.add_argument("--extract", type=str, metavar="FILE",
                        help="Extract information from guidelines document")
    
    args = parser.parse_args()
    
    if args.extract:
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
            output_format=args.format
        )
    else:
        run_interactive_mode()


if __name__ == "__main__":
    main()
