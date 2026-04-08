"""
Test Suite for Fishermen Alert System
Tests all components with various scenarios
"""

import unittest
from weather_api import get_mock_weather_data
from alert_engine import (
    generate_alert, 
    AlertLevel, 
    analyze_wind, 
    analyze_visibility,
    analyze_rain,
    analyze_condition
)
from nlp_generator import generate_nlp_message, generate_sms_alert


class TestWeatherAPI(unittest.TestCase):
    """Test cases for weather_api module."""
    
    def test_mock_data_normal(self):
        """Test normal scenario mock data."""
        data = get_mock_weather_data("Mumbai", "normal")
        self.assertEqual(data["location"], "Mumbai")
        self.assertEqual(data["wind_speed"], 15)
        self.assertEqual(data["condition"], "Clear")
    
    def test_mock_data_storm(self):
        """Test storm scenario mock data."""
        data = get_mock_weather_data("Chennai", "storm")
        self.assertEqual(data["location"], "Chennai")
        self.assertEqual(data["wind_speed"], 55)
        self.assertEqual(data["condition"], "Thunderstorm")
    
    def test_mock_data_all_scenarios(self):
        """Test all mock scenarios return valid data."""
        scenarios = ["normal", "windy", "storm", "heavy_rain"]
        for scenario in scenarios:
            data = get_mock_weather_data("Test", scenario)
            self.assertIsNotNone(data)
            self.assertIn("wind_speed", data)
            self.assertIn("temperature", data)
            self.assertIn("condition", data)


class TestAlertEngine(unittest.TestCase):
    """Test cases for alert_engine module."""
    
    def test_wind_analysis_safe(self):
        """Test safe wind speed detection."""
        level, reason = analyze_wind(10)
        self.assertEqual(level, AlertLevel.SAFE)
    
    def test_wind_analysis_caution(self):
        """Test caution wind speed detection."""
        level, reason = analyze_wind(25)
        self.assertEqual(level, AlertLevel.CAUTION)
    
    def test_wind_analysis_dangerous(self):
        """Test dangerous wind speed detection."""
        level, reason = analyze_wind(45)
        self.assertEqual(level, AlertLevel.DANGEROUS)
    
    def test_visibility_analysis(self):
        """Test visibility analysis."""
        # Good visibility
        level, _ = analyze_visibility(8)
        self.assertEqual(level, AlertLevel.SAFE)
        
        # Poor visibility
        level, _ = analyze_visibility(3)
        self.assertEqual(level, AlertLevel.CAUTION)
        
        # Very poor visibility
        level, _ = analyze_visibility(1)
        self.assertEqual(level, AlertLevel.DANGEROUS)
    
    def test_rain_analysis(self):
        """Test rain analysis."""
        # No rain
        level, _ = analyze_rain(0)
        self.assertEqual(level, AlertLevel.SAFE)
        
        # Moderate rain
        level, _ = analyze_rain(5)
        self.assertEqual(level, AlertLevel.CAUTION)
        
        # Heavy rain
        level, _ = analyze_rain(15)
        self.assertEqual(level, AlertLevel.DANGEROUS)
    
    def test_condition_analysis(self):
        """Test weather condition analysis."""
        # Safe condition
        level, _ = analyze_condition("Clear")
        self.assertEqual(level, AlertLevel.SAFE)
        
        # Caution condition
        level, _ = analyze_condition("Rain")
        self.assertEqual(level, AlertLevel.CAUTION)
        
        # Dangerous condition
        level, _ = analyze_condition("Thunderstorm")
        self.assertEqual(level, AlertLevel.DANGEROUS)
    
    def test_full_alert_safe(self):
        """Test full alert generation for safe conditions."""
        weather = get_mock_weather_data("Mumbai", "normal")
        alert = generate_alert(weather)
        
        self.assertEqual(alert["level"], AlertLevel.SAFE)
        self.assertEqual(alert["icon"], "✅")
        self.assertIn("SAFE", alert["title"])
    
    def test_full_alert_caution(self):
        """Test full alert generation for caution conditions."""
        weather = get_mock_weather_data("Chennai", "windy")
        alert = generate_alert(weather)
        
        self.assertEqual(alert["level"], AlertLevel.CAUTION)
        self.assertEqual(alert["icon"], "⚠️")
        self.assertIn("CAUTION", alert["title"])
    
    def test_full_alert_dangerous(self):
        """Test full alert generation for dangerous conditions."""
        weather = get_mock_weather_data("Kochi", "storm")
        alert = generate_alert(weather)
        
        self.assertEqual(alert["level"], AlertLevel.DANGEROUS)
        self.assertEqual(alert["icon"], "🚫")
        self.assertIn("DANGEROUS", alert["title"])
    
    def test_alert_with_none_data(self):
        """Test alert generation with None weather data."""
        alert = generate_alert(None)
        
        self.assertEqual(alert["level"], AlertLevel.CAUTION)
        self.assertIn("Unavailable", alert["title"])


class TestNLPGenerator(unittest.TestCase):
    """Test cases for nlp_generator module."""
    
    def test_english_message(self):
        """Test English message generation."""
        weather = get_mock_weather_data("Mumbai", "normal")
        message = generate_nlp_message(weather, AlertLevel.SAFE, "en")
        
        self.assertIn("Mumbai", message)
        self.assertIsInstance(message, str)
        self.assertTrue(len(message) > 10)
    
    def test_hindi_message(self):
        """Test Hindi message generation."""
        weather = get_mock_weather_data("Chennai", "windy")
        message = generate_nlp_message(weather, AlertLevel.CAUTION, "hi")
        
        self.assertIsInstance(message, str)
        self.assertTrue(len(message) > 10)
    
    def test_marathi_message(self):
        """Test Marathi message generation."""
        weather = get_mock_weather_data("Kochi", "storm")
        message = generate_nlp_message(weather, AlertLevel.DANGEROUS, "mr")
        
        self.assertIsInstance(message, str)
        self.assertTrue(len(message) > 10)
    
    def test_sms_alert_length(self):
        """Test SMS alert is within character limit."""
        weather = get_mock_weather_data("Mumbai", "storm")
        sms = generate_sms_alert(weather, AlertLevel.DANGEROUS, "en")
        
        # SMS should be concise (typically under 160 chars)
        self.assertTrue(len(sms) < 200)
    
    def test_sms_alert_all_languages(self):
        """Test SMS alert generation in all languages."""
        weather = get_mock_weather_data("Test", "normal")
        
        for lang in ["en", "hi", "mr"]:
            sms = generate_sms_alert(weather, AlertLevel.SAFE, lang)
            self.assertIsInstance(sms, str)
            self.assertTrue(len(sms) > 5)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_wind_boundary_conditions(self):
        """Test wind speed at exact boundary values."""
        # At safe threshold
        level, _ = analyze_wind(20)
        self.assertEqual(level, AlertLevel.CAUTION)
        
        # Just below safe threshold
        level, _ = analyze_wind(19.9)
        self.assertEqual(level, AlertLevel.SAFE)
        
        # At dangerous threshold
        level, _ = analyze_wind(35)
        self.assertEqual(level, AlertLevel.DANGEROUS)
    
    def test_empty_location(self):
        """Test with empty location string."""
        weather = get_mock_weather_data("", "normal")
        alert = generate_alert(weather)
        
        self.assertIsNotNone(alert)
        self.assertEqual(alert["location"], "")
    
    def test_invalid_scenario(self):
        """Test with invalid scenario falls back to normal."""
        weather = get_mock_weather_data("Test", "invalid_scenario")
        
        self.assertIsNotNone(weather)
        self.assertEqual(weather["wind_speed"], 15)  # Normal scenario default
    
    def test_zero_values(self):
        """Test with zero weather values."""
        weather = {
            "location": "Test",
            "wind_speed": 0,
            "temperature": 0,
            "condition": "Clear",
            "visibility": 10,
            "rain_1h": 0,
            "humidity": 0
        }
        alert = generate_alert(weather)
        
        self.assertEqual(alert["level"], AlertLevel.SAFE)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline."""
    
    def test_complete_pipeline_all_scenarios(self):
        """Test complete pipeline for all scenarios."""
        scenarios = ["normal", "windy", "storm", "heavy_rain"]
        expected_levels = [
            AlertLevel.SAFE,
            AlertLevel.CAUTION,
            AlertLevel.DANGEROUS,
            AlertLevel.DANGEROUS
        ]
        
        for scenario, expected in zip(scenarios, expected_levels):
            weather = get_mock_weather_data("Test", scenario)
            alert = generate_alert(weather)
            
            self.assertEqual(
                alert["level"], expected,
                f"Failed for scenario: {scenario}"
            )
            
            # Generate messages in all languages
            for lang in ["en", "hi", "mr"]:
                msg = generate_nlp_message(weather, alert["level"], lang)
                self.assertIsInstance(msg, str)
    
    def test_alert_contains_all_fields(self):
        """Test that alert contains all required fields."""
        weather = get_mock_weather_data("Mumbai", "normal")
        alert = generate_alert(weather)
        
        required_fields = [
            "level", "icon", "title", "message", 
            "reasons", "recommendation", "location", "details"
        ]
        
        for field in required_fields:
            self.assertIn(field, alert, f"Missing field: {field}")


def run_tests():
    """Run all tests with verbose output."""
    print("\n" + "=" * 60)
    print("🧪 FISHERMEN ALERT SYSTEM - TEST SUITE")
    print("=" * 60 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAlertEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestNLPGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
