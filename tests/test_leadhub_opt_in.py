import json
import unittest
from unittest.mock import MagicMock, patch

try:
    from app.utils.leadhub import get_related_products, subscribe_research_updates
except ModuleNotFoundError as exc:
    raise unittest.SkipTest(f"Install repository requirements first ({exc.name} is missing)") from exc


class LeadHubOptInTests(unittest.TestCase):
    @patch("app.utils.leadhub.urlopen")
    def test_related_products_send_only_the_product_id_after_explicit_opt_in(self, urlopen):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({"items": [
            {"id": "portfolio", "name": "YashRaj Studio", "url": "https://studio.example.test/", "reason": "Build support"},
            {"id": "unsafe", "name": "Unsafe", "url": "http://bad.example/", "reason": "Bad"},
        ]}).encode()
        urlopen.return_value = response

        items = get_related_products("https://leads.example.test/", "vitalcue")

        self.assertEqual([item["id"] for item in items], ["portfolio"])
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://leads.example.test/api/recommendations?project=vitalcue&consent=true")
        self.assertEqual(request.data, None)

    @patch("app.utils.leadhub.urlopen")
    def test_related_products_reject_unconfigured_origins(self, urlopen):
        self.assertEqual(get_related_products("http://leads.example.test", "vitalcue"), [])
        urlopen.assert_not_called()

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
