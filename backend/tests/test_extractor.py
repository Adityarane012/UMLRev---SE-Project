import os
import sys
import unittest

# Ensure UMLRev directory is on sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(TEST_DIR)
UMLREV_ROOT = os.path.dirname(BACKEND_DIR)
if UMLREV_ROOT not in sys.path:
    sys.path.insert(0, UMLREV_ROOT)

from backend.umlrev.pipeline.extractor import SymbolExtractor


class TestSymbolExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = SymbolExtractor()
        self.benchmark_path = os.path.join(UMLREV_ROOT, "examples", "tell_story")

    def test_extract_tell_story_classes(self):
        """Verifies that Tell Story benchmark discovers all 4 expected classes."""
        project = self.extractor.scan_directory(self.benchmark_path, "TellStoryTest")
        class_names = list(project.classes.keys())

        self.assertIn("Enemy", class_names)
        self.assertIn("Hero", class_names)
        self.assertIn("Princess", class_names)
        self.assertIn("Story", class_names)
        self.assertEqual(len(project.classes), 4)

    def test_extract_methods_and_relationships(self):
        """Verifies method symbols and structural relationships are correctly derived."""
        project = self.extractor.scan_directory(self.benchmark_path, "TellStoryTest")
        story_class = project.get_class("Story")
        self.assertIsNotNone(story_class)
        
        method_names = [m.name for m in story_class.methods]
        self.assertIn("start", method_names)
        self.assertIn("tell", method_names)
        self.assertGreater(len(project.relationships), 0)


if __name__ == "__main__":
    unittest.main()
