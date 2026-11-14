"""Cookieless PostHog settings for the public site.

The project token is a public client token. It is safe to ship in the browser,
and it is read from this module only. scripts/build-public.py (the Netlify
build) writes it into the generated public-site/assets/posthog-boot.js file.
Do not copy the token into other JavaScript sources.

Environment overrides (all optional):

  POSTHOG_TOKEN    project token (phc_...)
  POSTHOG_HOST     ingestion host, default https://us.i.posthog.com
  POSTHOG_UI_HOST  dashboard host, default https://us.posthog.com

POSTHOG_HOST should be a PostHog ingestion host such as
https://us.i.posthog.com. The official snippet loads array.js from the matching
assets host (https://us-assets.i.posthog.com).
"""
import os

_DEFAULT_TOKEN = "phc_poCZLhoegtPqHTzkh3JKQyx5JAmnKCmVzcSKeAT8tMKM"
_DEFAULT_HOST = "https://us.i.posthog.com"
_DEFAULT_UI_HOST = "https://us.posthog.com"


def _env(name, default):
    value = os.environ.get(name, "").strip()
    return value or default


def _https(url):
    if not url.startswith("https://") or any(c in url for c in " \t\r\n\"'"):
        raise SystemExit("PostHog host must be an https URL without spaces: " + url)
    return url.rstrip("/")


POSTHOG_TOKEN = _env("POSTHOG_TOKEN", _DEFAULT_TOKEN)
POSTHOG_HOST = _https(_env("POSTHOG_HOST", _DEFAULT_HOST))
POSTHOG_UI_HOST = _https(_env("POSTHOG_UI_HOST", _DEFAULT_UI_HOST))

if not POSTHOG_TOKEN.startswith("phc_") or len(POSTHOG_TOKEN) < 20:
    raise SystemExit("POSTHOG_TOKEN must be a PostHog project token (phc_...)")
