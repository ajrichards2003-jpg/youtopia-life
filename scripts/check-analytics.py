"""Static checks for cookieless PostHog. No network and no browser."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from analytics_config import POSTHOG_HOST, POSTHOG_TOKEN, POSTHOG_UI_HOST  # noqa: E402

consent = (ROOT / "assets" / "analytics-consent.js").read_text(encoding="utf-8")
assert "Cookieless PostHog analytics is used" in consent
assert "no cookies" in consent and "no\n * identifiers" in consent
assert "window.youtopiaCampaign = campaign" in consent
assert "awinaffid" in consent and "clickref" in consent
assert "utm_source" in consent and "youtopia-weekly" in consent
assert "phc_" not in consent

analytics = (ROOT / "assets" / "analytics.js").read_text(encoding="utf-8")
for event in ("affiliate_click", "form_submit", "video_play", "cta_click"):
    assert event in analytics, event
for banned in ("phc_", "localStorage", "sessionStorage", "document.cookie"):
    assert banned not in analytics, banned
assert "transport: 'sendBeacon'" in analytics or 'transport: "sendBeacon"' in analytics or "sendBeacon" in analytics
assert "youtopiaCampaign" in analytics
assert "ultrahuman.com" in analytics and "awin1.com" in analytics
for form in ("youtopia-weekly", "youtopia-contact", "first-collection-interest",
             "merch-interest", "wallpaper-signup", "youtopia-signup"):
    assert form in analytics, form
assert "data-netlify" in analytics

config = (ROOT / "tools" / "analytics_config.py").read_text(encoding="utf-8")
assert "POSTHOG_TOKEN" in config and "POSTHOG_HOST" in config
assert POSTHOG_TOKEN.startswith("phc_") and len(POSTHOG_TOKEN) > 20
assert POSTHOG_HOST == "https://us.i.posthog.com"
assert POSTHOG_UI_HOST == "https://us.posthog.com"
assert config.count(POSTHOG_TOKEN) == 1
template = (ROOT / "tools" / "posthog_boot_template.js").read_text(encoding="utf-8")
assert "phc_" not in template
for needle in ("cookieless_mode: 'always'", "persistence: 'memory'",
               "disable_session_recording: true", "autocapture: false",
               "capture_pageview: true", "capture_pageleave: true",
               "person_profiles: 'identified_only'", "respect_dnt: true",
               "__POSTHOG_TOKEN__", "-assets.i.posthog.com"):
    assert needle in template, needle

csp = (ROOT / "netlify.toml").read_text(encoding="utf-8")
policy = re.search(r'Content-Security-Policy-Report-Only = "(.*)"', csp)
assert policy, "report-only CSP missing"
for host in ("https://us.i.posthog.com", "https://us-assets.i.posthog.com"):
    assert policy.group(1).count(host) >= 2, host  # script-src and connect-src

privacy = (ROOT / "privacy" / "index.html").read_text(encoding="utf-8")
assert "cookieless PostHog analytics" in privacy
assert "no cookies and no identifiers" in privacy
assert "without placing analytics cookies" not in privacy
assert "loading a browser analytics tag" not in privacy

print("PASS: cookieless PostHog source checks")
