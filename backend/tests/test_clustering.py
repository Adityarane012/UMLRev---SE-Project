import os
import sys
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(TEST_DIR)
UMLREV_ROOT = os.path.dirname(BACKEND_DIR)
if UMLREV_ROOT not in sys.path:
    sys.path.insert(0, UMLREV_ROOT)

from backend.umlrev.model.symbol import ClassSymbol, Relationship
from backend.umlrev.pipeline.clustering import ClusterEngine


class TestClusterEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ClusterEngine()

    def test_empty_classes(self):
        clusters = self.engine.cluster([])
        self.assertEqual(len(clusters), 0)

    def test_benchmark_clustering(self):
        """Verifies that 4 tightly coupled benchmark classes form a cohesive cluster."""
        classes = [
            ClassSymbol(name="Story", file_path="Story.java"),
            ClassSymbol(name="Hero", file_path="Hero.java"),
            ClassSymbol(name="Enemy", file_path="Enemy.java"),
            ClassSymbol(name="Princess", file_path="Princess.java"),
        ]
        clusters = self.engine.cluster(classes)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(len(clusters[0].class_names()), 4)


if __name__ == "__main__":
    unittest.main()
