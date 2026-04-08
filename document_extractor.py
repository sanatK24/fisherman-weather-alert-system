import re
import os
from typing import Dict, List, Tuple, Optional
from collections import Counter


def simplify_sentence(sentence):
    replacements = {
        "must": "Always",
        "should": "Try to",
        "required": "You need to",
        "mandatory": "Must",
        "prohibited": "Do not",
        "forbidden": "Do not",
        "minimum": "At least",
        "maximum": "Up to",
        "vessel": "Boat",
        "communication": "Talk",
        "equipment": "Tools",
        "carry": "Take",
        "ensure": "Make sure",
        "prior to": "Before",
        "during": "While"
    }

    simple = sentence

    for word, replacement in replacements.items():
        simple = simple.replace(word, replacement)

    return simple


def shorten_sentence(sentence, max_words=12):
    words = sentence.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return sentence


# Keywords for different categories
SAFETY_KEYWORDS = [
    "danger", "warning", "caution", "alert", "emergency", "hazard", "risk",
    "unsafe", "prohibited", "forbidden", "avoid", "never", "don't", "do not",
    "life jacket", "vest", "safety gear", "first aid", "rescue", "sos",
    "खतरा", "सावधान", "चेतावनी", "धोका", "सावध"  # Hindi/Marathi
]

WEATHER_KEYWORDS = [
    "wind", "storm", "rain", "monsoon", "cyclone", "hurricane", "thunder",
    "lightning", "fog", "visibility", "tide", "wave", "current", "temperature",
    "forecast", "weather", "climate", "season", "summer", "winter",
    "हवा", "तूफान", "बारिश", "मौसम", "वारा", "पाऊस"  # Hindi/Marathi
]

REGULATION_KEYWORDS = [
    "license", "permit", "legal", "illegal", "law", "regulation", "rule",
    "fine", "penalty", "ban", "season", "quota", "limit", "size", "minimum",
    "maximum", "allowed", "permitted", "restricted", "zone", "area",
    "prohibited", "conservation", "protected", "species"
]

EQUIPMENT_KEYWORDS = [
    "net", "boat", "engine", "motor", "fuel", "anchor", "rope", "hook",
    "line", "rod", "reel", "bait", "trap", "gear", "equipment", "tool",
    "radio", "gps", "compass", "light", "torch", "battery"
]

EMERGENCY_KEYWORDS = [
    "emergency", "sos", "distress", "rescue", "coast guard", "helpline",
    "phone", "contact", "call", "radio", "signal", "flare", "help",
    "hospital", "medical", "injury", "accident", "drown", "capsize"
]


class DocumentExtractor:
    
    def __init__(self):
        self.categories = {
            "safety": SAFETY_KEYWORDS,
            "weather": WEATHER_KEYWORDS,
            "regulations": REGULATION_KEYWORDS,
            "equipment": EQUIPMENT_KEYWORDS,
            "emergency": EMERGENCY_KEYWORDS
        }
    
    def read_file(self, filepath: str) -> Optional[str]:
        try:
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            
            print(f"Could not read file with supported encodings")
            return None
            
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def extract_sentences(self, text: str) -> List[str]:
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        return sentences
    
    def categorize_sentence(self, sentence: str) -> List[str]:
        sentence_lower = sentence.lower()
        found_categories = []
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in sentence_lower:
                    found_categories.append(category)
                    break
        
        return found_categories
    
    def extract_numbers(self, text: str) -> List[Dict]:
        numbers = []
        
        patterns = [
            (r'(\d+)\s*(km/h|kmph|mph)', 'speed'),
            (r'(\d+)\s*(km|kilometer|kilometre|meter|metre|m|feet|ft)', 'distance'),
            (r'(\d+)\s*(kg|kilogram|gram|g|pound|lb)', 'weight'),
            (r'(\d+)\s*(cm|inch|inches|mm)', 'size'),
            (r'(\d+)\s*(hour|hr|minute|min|day|week|month)', 'time'),
            (r'₹?\s*(\d+[\d,]*)', 'amount'),
            (r'(\d{10})', 'phone'),
        ]
        
        for pattern, num_type in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                numbers.append({
                    "value": match.group(0),
                    "type": num_type,
                    "context": text[max(0, match.start()-30):min(len(text), match.end()+30)]
                })
        
        return numbers
    
    def extract_contacts(self, text: str) -> List[Dict]:
        contacts = []
        
        phone_patterns = [
            r'\b(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b',
            r'\b(\d{10,11})\b',
            r'\b(\d{4}[-.\s]?\d{6})\b',
            r'\b(1\d{2,3})\b',
        ]
        
        for pattern in phone_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 20)
                context = text[start:end].strip()
                
                contacts.append({
                    "number": match.group(1),
                    "context": context
                })
        
        return contacts
    
    def extract_key_points(self, text: str) -> Dict[str, List[str]]:
        sentences = self.extract_sentences(text)
        
        categorized = {
            "safety": [],
            "weather": [],
            "regulations": [],
            "equipment": [],
            "emergency": [],
            "general": []
        }
        
        for sentence in sentences:
            categories = self.categorize_sentence(sentence)
            
            if categories:
                for cat in categories:
                    if sentence not in categorized[cat]:
                        simple_sentence = simplify_sentence(sentence)
                        simple_sentence = shorten_sentence(simple_sentence)
                        categorized[cat].append(simple_sentence)
            else:
                action_words = ["must", "should", "always", "never", "required", "important"]
                if any(word in sentence.lower() for word in action_words):
                    simple_sentence = simplify_sentence(sentence)
                    simple_sentence = shorten_sentence(simple_sentence)
                    categorized["general"].append(simple_sentence)
        
        return {k: v for k, v in categorized.items() if v}
    
    def generate_summary(self, text: str) -> Dict:
        key_points = self.extract_key_points(text)
        numbers = self.extract_numbers(text)
        contacts = self.extract_contacts(text)
        
        words = text.lower().split()
        word_count = len(words)
        
        important_words = [w for w in words if len(w) > 4]
        common_words = Counter(important_words).most_common(10)
        
        return {
            "statistics": {
                "total_words": word_count,
                "total_sentences": len(self.extract_sentences(text)),
                "categories_found": list(key_points.keys())
            },
            "key_points": key_points,
            "important_numbers": numbers[:10],
            "emergency_contacts": contacts,
            "common_topics": common_words
        }
    
    def format_summary_for_display(self, summary: Dict) -> str:
        lines = [
            "\nDOCUMENT ANALYSIS SUMMARY\n",
            f"Statistics:",
            f"   • Total words: {summary['statistics']['total_words']}",
            f"   • Total sentences: {summary['statistics']['total_sentences']}",
            f"   • Categories found: {', '.join(summary['statistics']['categories_found'])}"
        ]
        
        lines.append("\nKEY POINTS BY CATEGORY")
        
        category_icons = {
            "safety": "SAFETY",
            "weather": "WEATHER",
            "regulations": "REGULATIONS",
            "equipment": "EQUIPMENT",
            "emergency": "EMERGENCY",
            "general": "GENERAL"
        }
        
        for category, points in summary['key_points'].items():
            icon = category_icons.get(category, f"{category.upper()}")
            lines.append(f"\n{icon}:")
            for i, point in enumerate(points[:5], 1):
                if len(point) > 100:
                    point = point[:100] + "..."
                lines.append(f"   {i}. {point}")
        
        if summary['emergency_contacts']:
            lines.append("\nEMERGENCY CONTACTS FOUND")
            seen = set()
            for contact in summary['emergency_contacts'][:5]:
                if contact['number'] not in seen:
                    lines.append(f"   • {contact['number']}: {contact['context'][:50]}...")
                    seen.add(contact['number'])
        
        if summary['important_numbers']:
            lines.append("\nIMPORTANT NUMBERS/LIMITS")
            seen = set()
            for num in summary['important_numbers']:
                if num['value'] not in seen:
                    lines.append(f"   • {num['value']} ({num['type']})")
                    seen.add(num['value'])
        
        return "\n".join(lines)


def extract_from_file(filepath: str) -> Optional[Dict]:
    extractor = DocumentExtractor()
    
    text = extractor.read_file(filepath)
    if text is None:
        return None
    
    summary = extractor.generate_summary(text)
    
    return summary


def extract_from_text(text: str) -> Dict:
    extractor = DocumentExtractor()
    return extractor.generate_summary(text)


if __name__ == "__main__":
    sample_text = """
    FISHING SAFETY GUIDELINES
    
    WARNING: Always check weather forecast before going to sea. Wind speeds above 40 km/h 
    are dangerous for small boats. Never go fishing alone.
    
    SAFETY EQUIPMENT:
    - Life jacket must be worn at all times
    - Carry a first aid kit
    - GPS device recommended for navigation
    - Minimum boat length: 15 feet
    
    EMERGENCY CONTACTS:
    - Coast Guard: 1554
    - Marine Police: 100
    - Emergency Helpline: 108
    - Fisheries Department: 1800-123-4567
    
    REGULATIONS:
    - Fishing license required (Fine: ₹5000 for violation)
    - Minimum fish size: 25 cm
    - Prohibited during monsoon season (June-August)
    - Maximum catch limit: 50 kg per day
    
    WEATHER ALERTS:
    - Red flag: Do not venture into sea
    - Yellow flag: Exercise caution
    - Green flag: Safe for fishing
    
    खतरा: तूफान के दौरान समुद्र में न जाएं।
    सावधान: जीवन रक्षक जैकेट हमेशा पहनें।
    """
    
    print("Testing Document Extractor with sample fishing guidelines...")
    
    extractor = DocumentExtractor()
    summary = extractor.generate_summary(sample_text)
    print(extractor.format_summary_for_display(summary))
