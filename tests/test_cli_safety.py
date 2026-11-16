import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

try:
    from app.services import newpatient
except ModuleNotFoundError as exc:
    raise unittest.SkipTest(f"Install repository requirements first ({exc.name} is missing)") from exc


class FictionalCliTests(unittest.TestCase):
    @patch("app.services.newpatient.process_patient")
    def test_cli_uses_fixed_fictional_values_without_storage_or_side_effects(self, process):
        process.return_value.risk_label = "Low"
        process.return_value.bmi = 22.5
        output = StringIO()

        with redirect_stdout(output):
            newpatient.main()

        args, kwargs = process.call_args
        self.assertEqual(args, (65, 80, 120, 180, 65, 1.7))
        self.assertEqual(
            kwargs,
            {"save_to_db": False, "generate_pdf": False, "send_alert": False},
        )
        self.assertIn("fictional sample", output.getvalue())
        self.assertIn("No values were saved", output.getvalue())


if __name__ == "__main__":
    unittest.main()
