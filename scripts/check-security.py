"""Youtopia deployment safety checks. Fail closed for high-risk configuration regressions."""
from pathlib import Path
import re
import tomllib

root = Path(__file__).resolve().parents[1]
config = tomllib.loads((root / "netlify.toml").read_text())
build = config["build"]
assert build["publish"] == "public-site", "Never deploy the repo root"
assert build["functions"] == "netlify/functions"
assert "scripts/build-public.py" in build["command"]

api = (root / "netlify/functions/ask-youtopia.mjs").read_text()
assert 'path: "/api/ask-youtopia"' in api, "Function must use one canonical route"
assert 'rateLimit:' in api and 'aggregateBy: ["ip", "domain"]' in api
assert re.search(r"windowLimit:\s*20\b", api)
assert "MAX_BODY_BYTES" in api and "ALLOWED_ORIGINS" in api
assert "getUser()" in api and "DAILY_LIMIT" in api
assert 'max_output_tokens: 500' in api
for key, value in {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "content-security-policy": "default-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
    "cross-origin-resource-policy": "same-origin",
    "referrer-policy": "no-referrer",
    "x-content-type-options": "nosniff",
    "x-frame-options": "DENY",
    "x-robots-tag": "noindex, nofollow",
}.items():
    expected = f'"{key}": "{value}"'
    assert expected in api, f"Missing function response security header: {key}"

routes = config.get("redirects", [])
assert not any(x.get("from") == "/api/ask-youtopia" for x in routes), "Don't reintroduce a redirect bypass"
headers = next(x["values"] for x in config["headers"] if x["for"] == "/*")
for key in ("Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy", "Permissions-Policy"):
    assert key in headers, f"Missing response security header: {key}"
assert headers["X-Content-Type-Options"] == "nosniff"
assert "max-age=" in headers["Strict-Transport-Security"]
assert "default-src" in headers["Content-Security-Policy-Report-Only"]

public = root / "public-site"
if public.exists():
    forbidden_extensions = {".env", ".toml", ".yaml", ".yml", ".md", ".py", ".map", ".sh", ".patch"}
    forbidden_names = {"package.json", "package-lock.json", "secrets.json", ".env"}
    for item in public.rglob("*"):
        if not item.is_file():
            continue
        assert item.suffix.lower() not in forbidden_extensions, f"Private file in publish directory: {item.relative_to(public)}"
        assert item.name.lower() not in forbidden_names, f"Private file in publish directory: {item.relative_to(public)}"
    assert (public / "index.html").is_file()
    assert not (public / "netlify").exists()
print("PASS: security routing, headers, public-only output and AI safeguards")
