"""Server-side opt-in signup for the separate research mailing list."""
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


def _https_origin(base_url):
    try:
        parsed = urlparse((base_url or "").strip())
    except ValueError:
        return ""
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        return ""
    return f"https://{parsed.netloc}"


def is_configured(base_url):
    return bool(_https_origin(base_url))


def _safe_recommendation(item):
    if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in ("name", "reason", "url")):
        return False
    try:
        parsed = urlparse(item["url"])
        hostname = parsed.hostname or ""
        return (
            parsed.scheme == "https"
            and hostname
            and not parsed.username
            and not parsed.password
            and hostname != "example.com"
            and not hostname.endswith(".example.com")
        )
    except ValueError:
        return False


def get_related_products(base_url, project):
    origin = _https_origin(base_url)
    if not origin:
        return []
    query = urlencode({"project": project, "consent": "true"})
    request = Request(f"{origin}/api/recommendations?{query}", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=5) as response:
            result = json.loads(response.read())
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return []
    items = result.get("items", []) if isinstance(result, dict) else []
    return [item for item in items if _safe_recommendation(item)] if isinstance(items, list) else []


def subscribe_research_updates(email, consent, base_url, source):
    origin = _https_origin(base_url)
    address = (email or "").strip().lower()
    if not origin:
        return False, "Signup is not configured yet."
    if not consent:
        return False, "Please opt in before joining the research list."
    if len(address) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", address):
        return False, "Enter a valid email address."

    payload = {
        "project": "vitalcue",
        "email": address,
        "consent": True,
        "website": "",
        "source": source,
    }
    request = Request(
        f"{origin}/api/subscribe",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=8) as response:
            result = json.loads(response.read())
        if result.get("ok"):
            return True, result.get("message", "Check your inbox to confirm your signup.")
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        pass
    return False, "Signup is unavailable right now. Please try again later."
