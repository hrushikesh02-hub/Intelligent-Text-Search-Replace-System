import unittest
import re
from core.regex_engine import create_pattern, count_matches, replace_text, get_match_details

class TestRegexEngine(unittest.TestCase):
    
    def test_email_matching(self):
        pattern = create_pattern(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", True, False)
        text = "Contact us at info@example.com or support@test.org."
        self.assertEqual(count_matches(text, pattern), 2)
        
    def test_phone_matching(self):
        pattern = create_pattern(r"\b\d{10}\b", True, False)
        text = "My number is 1234567890 and hers is 0987654321."
        self.assertEqual(count_matches(text, pattern), 2)
        
    def test_number_matching(self):
        pattern = create_pattern(r"\b\d+\b", True, False)
        text = "There are 5 apples and 20 oranges."
        self.assertEqual(count_matches(text, pattern), 2)
        
    def test_date_matching(self):
        pattern = create_pattern(r"\b\d{2}/\d{2}/\d{4}\b", True, False)
        text = "Start date: 01/01/2025, End date: 31/12/2025"
        self.assertEqual(count_matches(text, pattern), 2)
        
    def test_case_insensitive(self):
        pattern = create_pattern(r"hello", True, True)
        text = "Hello there, hello world."
        self.assertEqual(count_matches(text, pattern), 2)
        
    def test_invalid_regex(self):
        with self.assertRaises(re.error):
            create_pattern(r"[Unclosed bracket", True, False)
            
    def test_literal_search(self):
        pattern = create_pattern(r"C:\temp", False, False)
        text = r"Path is C:\temp and C:\temp\dir"
        self.assertEqual(count_matches(text, pattern), 2)
        
    def test_replacement_count(self):
        pattern = create_pattern(r"\b\d{10}\b", True, False)
        text = "Call 1234567890 or 9876543210."
        new_text, count = replace_text(text, pattern, "[PHONE]")
        self.assertEqual(count, 2)
        self.assertEqual(new_text, "Call [PHONE] or [PHONE].")
        
    def test_whole_word(self):
        pattern = create_pattern("apple", False, True, True)
        text = "apple pineapple applesauce APPLE"
        count, details = get_match_details(text, pattern)
        self.assertEqual(count, 2)
        self.assertEqual(details[0]['matched_text'].lower(), "apple")
        self.assertEqual(details[1]['matched_text'].lower(), "apple")

    def test_get_match_details(self):
        pattern = create_pattern("cat", False, False, False)
        text = "cat\nbobcat\nCAT"
        count, details = get_match_details(text, pattern, "[DOG]")
        self.assertEqual(count, 2)
        self.assertEqual(details[1]['line'], 2)
        self.assertEqual(details[1]['position'], 4)
        self.assertEqual(details[1]['replacement'], "[DOG]")

if __name__ == '__main__':
    unittest.main()
