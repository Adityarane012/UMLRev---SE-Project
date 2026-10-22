import os
import sys
import unittest
import io
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
    """
    Formal Test Suite executing Experiment 9 Test Cases (TC-01 to TC-04)
    for the UMLRev system.
    """

    def setUp(self):
        self.client = TestClient(app)
        self.benchmark_path = os.path.join(UMLREV_ROOT, "examples", "tell_story")
        # Ensure offline deterministic heuristic is used during automated test runs
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
        self.assertIn("Aditya Rane (B129)", data.get("team", []))

    # =========================================================================
    # TC-01: Login and dashboard access
    # =========================================================================
    def test_tc01_login_and_dashboard_access(self):
        """
        TC-01: Verifies user authentication, token issuance,
        and developer dashboard profile access.
        """
        # Step 1 & 2: Submit valid user credentials
        login_res = self.client.post(
            "/api/auth/login",
            json={"username": "aditya", "password": "password123"}
        )
        self.assertEqual(login_res.status_code, 200, "Authentication should return HTTP 200 OK")
        login_data = login_res.json()
        self.assertIn("token", login_data)
        self.assertTrue(login_data["token"].startswith("token-"))
        self.assertEqual(login_data.get("username"), "aditya")
        self.assertNotIn("role", login_data)

        # Step 3: Verify dashboard identity profile
        profile_res = self.client.get("/api/auth/me")
        self.assertEqual(profile_res.status_code, 200)
        profile_data = profile_res.json()
        self.assertTrue(profile_data.get("authenticated"))
        self.assertNotIn("role", profile_data)
        self.assertEqual(profile_data.get("name"), "Aditya Rane")

    # =========================================================================
    # TC-02: Repository validation
    # =========================================================================
    def test_tc02_repository_validation_negative_cases(self):
        """
        TC-02: Negative-input test verifying that invalid repository URLs,
        non-existent paths, and unsupported upload data are rejected with HTTP 400.
        """
        # Test Case 2a: Invalid remote repository URL
        invalid_url_res = self.client.post(
            "/api/projects/github",
            json={"github_url": "https://not-github.org/invalid/repo"}
        )
        self.assertEqual(invalid_url_res.status_code, 400)
        self.assertIn("Invalid GitHub URL", invalid_url_res.json().get("detail", ""))

        # Test Case 2b: Non-existent local directory path
        nonexistent_path = os.path.join(UMLREV_ROOT, "does_not_exist_xyz123")
        invalid_path_res = self.client.post(
            "/api/projects/create",
            data={"name": "Bad Path Project", "local_path": nonexistent_path}
        )
        self.assertEqual(invalid_path_res.status_code, 400)
        self.assertIn("Local path does not exist", invalid_path_res.json().get("detail", ""))

        # Test Case 2c: Unsupported upload format (non-zip file)
        fake_txt_file = io.BytesIO(b"Dummy non-zip text content")
        invalid_upload_res = self.client.post(
            "/api/projects/upload-zip",
            data={"name": "Invalid File Test"},
            files={"file": ("test.txt", fake_txt_file, "text/plain")}
        )
        self.assertEqual(invalid_upload_res.status_code, 400)
        self.assertIn("Unsupported upload", invalid_upload_res.json().get("detail", ""))

    # =========================================================================
    # TC-03: AI feature identification and review
    # =========================================================================
    def test_tc03_ai_feature_identification_and_review(self):
        """
        TC-03: Integration test verifying AI-suggested feature clustering,
        developer modifications, and formal approval persistence.
        """
        # Step 1: Initialize project with valid benchmark repository
        create_res = self.client.post(
            "/api/projects/create",
            data={"name": "Feature Review Test", "local_path": self.benchmark_path}
        )
        self.assertEqual(create_res.status_code, 200)
        proj_id = create_res.json()["project_id"]

        # Step 2: Trigger AI analysis to produce feature suggestions
        analyze_res = self.client.post(f"/api/projects/{proj_id}/analyze")
        self.assertEqual(analyze_res.status_code, 200)
        analyze_data = analyze_res.json()
        features = analyze_data.get("features", [])
        self.assertGreater(len(features), 0, "AI pipeline must discover at least 1 feature")
        self.assertEqual(features[0]["name"], "Tell Story")
        self.assertGreater(features[0]["confidence"], 0.80)

        # Step 3 & 4: Modify suggestion (Developer Human-in-the-Loop review) and approve
        updated_features_payload = [
            {
                "name": "Story Narrative & Combat Engine",
                "description": "Reviewed and approved domain feature orchestrating story quests.",
                "classes": ["Enemy", "Hero", "Princess", "Story"],
                "confidence": 0.99
            }
        ]
        update_res = self.client.put(
            f"/api/projects/{proj_id}/features",
            json=updated_features_payload
        )
        self.assertEqual(update_res.status_code, 200)
        update_data = update_res.json()
        self.assertEqual(update_data.get("status"), "updated")
        self.assertTrue(update_data.get("approved"))
        self.assertEqual(update_data["features"][0]["name"], "Story Narrative & Combat Engine")

        # Step 5: Verify persisted review state on GET
        fetch_res = self.client.get(f"/api/projects/{proj_id}/features")
        self.assertEqual(fetch_res.status_code, 200)
        fetch_data = fetch_res.json()
        self.assertEqual(fetch_data["features"][0]["name"], "Story Narrative & Combat Engine")

    # =========================================================================
    # TC-04: UML diagram generation
    # =========================================================================
    def test_tc04_uml_diagram_generation(self):
        """
        TC-04: End-to-end test verifying structural (Class) and behavioral (Sequence)
        UML diagram synthesis in PlantUML and Mermaid formats.
        """
        # Step 1: Initialize and analyze benchmark
        create_res = self.client.post(
            "/api/projects/create",
            data={"name": "Diagram Synthesis Test", "local_path": self.benchmark_path}
        )
        proj_id = create_res.json()["project_id"]
        self.client.post(f"/api/projects/{proj_id}/analyze")

        # Step 2: Fetch synthesized diagrams
        diagrams_res = self.client.get(f"/api/projects/{proj_id}/diagrams")
        self.assertEqual(diagrams_res.status_code, 200)
        diag_data = diagrams_res.json()
        diagrams = diag_data.get("diagrams", [])
        self.assertGreaterEqual(len(diagrams), 2, "Must generate both Class and Sequence diagrams")

        kinds = [d["kind"] for d in diagrams]
        self.assertIn("CLASS", kinds, "Class diagram must be present")
        self.assertIn("SEQUENCE", kinds, "Sequence diagram must be present")

        # Step 3: Verify syntax integrity for both formats
        class_diag = next(d for d in diagrams if d["kind"] == "CLASS")
        self.assertTrue(class_diag["uml_text"].startswith("@startuml"))
        self.assertTrue(class_diag["uml_text"].strip().endswith("@enduml"))
        self.assertIn("classDiagram", class_diag["svg_content"])

        seq_diag = next(d for d in diagrams if d["kind"] == "SEQUENCE")
        self.assertTrue(seq_diag["uml_text"].startswith("@startuml"))
        self.assertTrue(seq_diag["uml_text"].strip().endswith("@enduml"))
        self.assertIn("sequenceDiagram", seq_diag["svg_content"])


if __name__ == "__main__":
    unittest.main()
