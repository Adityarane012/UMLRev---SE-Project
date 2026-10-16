import os
import sys
import unittest
from fastapi.testclient import TestClient

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(TEST_DIR)
UMLREV_ROOT = os.path.dirname(BACKEND_DIR)
if UMLREV_ROOT not in sys.path:
    sys.path.insert(0, UMLREV_ROOT)

from unittest.mock import patch
from backend.umlrev.api.app import app
from backend.umlrev.pipeline.llm_client import LLMClient


class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.benchmark_path = os.path.join(UMLREV_ROOT, "examples", "tell_story")
        # Ensure offline deterministic heuristic is used during tests
        self.llm_patcher = patch.object(
            LLMClient,
            "ask",
            side_effect=lambda prompt: LLMClient._heuristic_fallback(None, prompt)
        )
        self.llm_patcher.start()

    def tearDown(self):
        self.llm_patcher.stop()

    def test_root_endpoint(self):
        """Verifies health check endpoint returns 200 and team info."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "online")
        self.assertIn("Jay Gandhi (B124)", data.get("team", []))

    def test_login_endpoint(self):
        """Verifies login endpoint provides authentication token."""
        response = self.client.post("/api/auth/login", json={"username": "aditya", "password": "password123"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("token", data)
        self.assertEqual(data.get("username"), "aditya")

    def test_project_lifecycle_with_benchmark(self):
        """End-to-end integration test: create project, analyze, fetch features and diagrams."""
        # 1. Create project with benchmark path
        create_res = self.client.post(
            "/api/projects/create",
            data={"name": "API Benchmark Test", "local_path": self.benchmark_path}
        )
        self.assertEqual(create_res.status_code, 200)
        proj_id = create_res.json()["project_id"]

        # 2. Analyze project
        analyze_res = self.client.post(f"/api/projects/{proj_id}/analyze")
        self.assertEqual(analyze_res.status_code, 200)
        analyze_data = analyze_res.json()
        self.assertGreater(len(analyze_data.get("features", [])), 0)

        # 3. Retrieve generated diagrams
        diagrams_res = self.client.get(f"/api/projects/{proj_id}/diagrams")
        self.assertEqual(diagrams_res.status_code, 200)
        diag_data = diagrams_res.json()
        self.assertGreater(len(diag_data.get("diagrams", [])), 0)


if __name__ == "__main__":
    unittest.main()
