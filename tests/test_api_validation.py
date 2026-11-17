import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from app.routes.api import app


class ApiValidationTests(unittest.TestCase):
    def setUp(self):
        self.auth_token = "t" * 32
        self.auth_patch = patch("app.routes.api.API_AUTH_TOKEN", self.auth_token)
        self.auth_patch.start()
        self.client = app.test_client()

    def tearDown(self):
        self.auth_patch.stop()

    def post_json(self, data):
        return self.client.post(
            "/predict",
            json=data,
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

    def test_records_requires_auth_and_bounds_the_requested_page(self):
        with patch("app.routes.api.API_RECORDS_ENABLED", True):
            unauthorized = self.client.get("/records")
            oversized = self.client.get(
                "/records?limit=101",
                headers={"Authorization": f"Bearer {self.auth_token}"},
            )
        self.assertEqual(unauthorized.status_code, 401)
        self.assertEqual(unauthorized.headers["Cache-Control"], "no-store")
        self.assertEqual(unauthorized.headers["WWW-Authenticate"], "Bearer")

        self.assertEqual(oversized.status_code, 400)
        self.assertEqual(oversized.get_json(), {"error": "limit must be an integer between 1 and 100"})
        self.assertEqual(oversized.headers["Cache-Control"], "no-store")

    def test_records_are_disabled_by_default_even_with_a_valid_token(self):
        with patch("app.routes.api.API_RECORDS_ENABLED", False):
            response = self.client.get(
                "/records", headers={"Authorization": f"Bearer {self.auth_token}"}
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Records endpoint is disabled"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_api_fails_closed_when_authentication_is_not_configured(self):
        with patch("app.routes.api.API_AUTH_TOKEN", "short"):
            response = self.client.get("/records", headers={"Authorization": f"Bearer {self.auth_token}"})

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json(), {"error": "API authentication is not configured"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_non_object_json_returns_a_json_client_error(self):
        response = self.client.post(
            "/predict",
            data="not-json",
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Request body must be a JSON object"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    def test_oversized_json_returns_a_bounded_json_error(self):
        response = self.client.post(
            "/predict",
            data=b'{"payload":"' + b"x" * (16 * 1024) + b'"}',
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

        self.assertEqual(response.status_code, 413)
        self.assertEqual(
            response.get_json(),
            {"error": "Request body must be 16 KiB or smaller"},
        )
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    def test_unknown_fields_are_rejected(self):
        response = self.post_json({
            "age": 65, "heart_rate": 80, "systolic_bp": 120,
            "cholesterol": 180, "weight": 65, "height": 1.7,
            "synthetic_data_confirmed": True,
            "send_alert": True,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Unknown fields: send_alert"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_prediction_requires_explicit_synthetic_data_confirmation(self):
        payload = {
            "age": 65, "heart_rate": 80, "systolic_bp": 120,
            "cholesterol": 180, "weight": 65, "height": 1.7,
        }
        for value in (None, False, "true"):
            with self.subTest(value=value), patch("app.routes.api.process_patient") as process_patient:
                if value is not None:
                    payload["synthetic_data_confirmed"] = value
                response = self.post_json(payload)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "synthetic_data_confirmed must be true; use fictional sample data only"},
                )
                process_patient.assert_not_called()
                payload.pop("synthetic_data_confirmed", None)

    def test_non_boolean_privacy_flags_return_a_client_error(self):
        response = self.post_json({
            "age": 65,
            "heart_rate": 80,
            "systolic_bp": 120,
            "cholesterol": 180,
            "weight": 65,
            "height": 1.7,
            "synthetic_data_confirmed": True,
            "save_to_db": "false",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "save_to_db must be a boolean"})

    def test_prediction_api_rejects_database_storage(self):
        response = self.post_json({
            "age": 65, "heart_rate": 80, "systolic_bp": 120,
            "cholesterol": 180, "weight": 65, "height": 1.7,
            "synthetic_data_confirmed": True,
            "save_to_db": True,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "API database storage is disabled"})

    def test_requested_pdf_is_returned_and_temporary_file_is_removed(self):
        payload = {
            "age": 65, "heart_rate": 80, "systolic_bp": 120,
            "cholesterol": 180, "weight": 65, "height": 1.7,
            "synthetic_data_confirmed": True,
            "generate_pdf": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.pdf"
            report.write_bytes(b"%PDF-test")
            result = SimpleNamespace(
                patient_id=None, risk_label="Low", bmi=22.49, health_score=100,
                food_plan="Example", exercise_plan="Example", pdf_file=str(report),
                email_sent=False,
            )
            with patch("app.routes.api.process_patient", return_value=result):
                response = self.post_json(payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        self.assertEqual(response.data, b"%PDF-test")
        self.assertEqual(response.headers["X-AgeWell-Risk"], "Low")
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertFalse(report.exists())

    def test_json_prediction_response_carries_research_only_disclaimer(self):
        payload = {
            "age": 65, "heart_rate": 80, "systolic_bp": 120,
            "cholesterol": 180, "weight": 65, "height": 1.7,
            "synthetic_data_confirmed": True,
        }
        result = SimpleNamespace(
            patient_id=None, risk_label="Low", bmi=22.49, health_score=100,
            food_plan="Example", exercise_plan="Example", pdf_file=None,
            email_sent=False,
        )
        with patch("app.routes.api.process_patient", return_value=result):
            response = self.post_json(payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn("not clinically validated", response.get_json()["disclaimer"])
        self.assertIn("Synthetic inputs only", response.get_json()["disclaimer"])


if __name__ == "__main__":
    unittest.main()
