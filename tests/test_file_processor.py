import unittest
import os
import tempfile
from core.file_processor import read_file, write_file, process_file_search, process_file_replace
from utils.backup import create_backup

class TestFileProcessor(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("Hello 1234567890 World!")
            
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def test_read_file(self):
        content, error = read_file(self.test_file)
        self.assertIsNone(error)
        self.assertEqual(content, "Hello 1234567890 World!")
        
    def test_search_file(self):
        res = process_file_search(self.test_file, r"\d+", True, False, False)
        self.assertEqual(res['status'], 'SUCCESS')
        self.assertEqual(res['matches'], 1)
        
    def test_replace_file(self):
        res = process_file_replace(self.test_file, r"\d+", "[NUM]", True, False, False)
        self.assertEqual(res['status'], 'SUCCESS')
        self.assertEqual(res['matches'], 1)
        self.assertEqual(res['replacements'], 1)
        
        content, _ = read_file(self.test_file)
        self.assertEqual(content, "Hello [NUM] World!")
        
    def test_handle_missing_file(self):
        res = process_file_search(os.path.join(self.temp_dir.name, "missing.txt"), "hello", False, False, False)
        self.assertEqual(res['status'], 'ERROR')
        
    def test_backup_creation(self):
        backup_file = create_backup(self.test_file)
        self.assertTrue(os.path.exists(backup_file))
        content, _ = read_file(backup_file)
        self.assertEqual(content, "Hello 1234567890 World!")

if __name__ == '__main__':
    unittest.main()
