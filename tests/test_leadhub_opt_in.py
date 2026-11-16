import json
import unittest
from unittest.mock import MagicMock, patch

try:
    from app.utils.leadhub import subscribe_research_updates
except ModuleNotFoundError as exc:
    raise unittest.SkipTest(f"Install repository requirements first ({exc.name} is missing)") from exc


class LeadHubOptInTests(unittest.TestCase):
    @patch("app.utils.leadhub.urlopen")
    def test_invalid_or_unconsented_signup_never_contacts_leadhub(self, urlopen):
        self.assertFalse(subscribe_research_updates("person@example.com", True, "http://leads.test", "demo")[0])
        self.assertFalse(subscribe_research_updates("person@example.com", False, "https://leads.test", "demo")[0])
        self.assertFalse(subscribe_research_updates("not-email", True, "https://leads.test", "demo")[0])
        urlopen.assert_not_called()

    @patch("app.utils.leadhub.urlopen")
    def test_signup_sends_email_and_consent_only_not_health_values(self, urlopen):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({"ok": True, "message": "Check your inbox."}).encode()
        urlopen.return_value = response

        success, message = subscribe_research_updates(
            " Learner@Example.com ", True, "https://leads.example.test/", "vitalcue-demo"
        )

        self.assertTrue(success)
        self.assertEqual(message, "Check your inbox.")
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(
            payload,
            {
                "project": "vitalcue",
                "email": "learner@example.com",
                "consent": True,
                "website": "",
                "source": "vitalcue-demo",
            },
        )


if __name__ == "__main__":
    unittest.main()
