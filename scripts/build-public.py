#!/usr/bin/env python3
"""Copy only public website files into Netlify's publish directory.

Do not deploy the repository root: it also contains private planning material,
scripts, PR notes, package manifests and internal QA documents.
"""
import json
import re
import sys
from pathlib import Path
from shutil import copy2, rmtree
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public-site"
sys.path.insert(0, str(ROOT / "tools"))
from analytics_config import POSTHOG_HOST, POSTHOG_TOKEN, POSTHOG_UI_HOST  # noqa: E402

# The repository also contains operational material that must never be served.
BLOCKED_DIRS = {
    ".git", ".github", ".netlify", ".vscode", "__pycache__", "node_modules",
    "scripts", "docs", "audit", "audits", "tests", "test", "tools", "netlify",
    "tmp", "temp", ".cache", "dist", "public-site",
}
ROOT_ALLOWED = {"index.html", "404.html", "books.html",
                "robots.txt", "ads.txt", "sitemap.xml",
                "favicon.ico", "manifest.webmanifest"}
PUBLIC_EXTS = {
    ".html", ".css", ".js", ".svg", ".webp", ".jpg", ".jpeg", ".png",
    ".gif", ".ico", ".avif", ".woff", ".woff2", ".mp4", ".webm",
    ".ogg", ".webmanifest", ".pdf",
}

# Unconfirmed partner pages are not published (302 to /shop/ in netlify.toml).
GATED = ("products/otra/", "products/aeternum/", "products/einstar/", "products/ape-born/", "products/sinocare/",
         "articles/sinocare-home-monitoring.html", "articles/ape-born-muscle-stimulation.html", "articles/otra-eyewear-style-guide.html")

if PUBLIC.exists():
    rmtree(PUBLIC)
PUBLIC.mkdir(parents=True)

count = 0
for source in ROOT.rglob("*"):
    if not source.is_file():
        continue
    rel = source.relative_to(ROOT)
    if any(p.startswith(".") or p in BLOCKED_DIRS for p in rel.parts[:-1]):
        continue
    if rel.parts[0] in BLOCKED_DIRS or source.name.startswith("."):
        continue
    # No scripts, source maps, .md/.yaml/.toml or application configuration.
    if len(rel.parts) == 1:
        if source.name not in ROOT_ALLOWED:
            continue
    elif source.suffix.lower() not in PUBLIC_EXTS:
        continue
    if rel.as_posix().startswith(GATED):
        continue
    target = PUBLIC / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, target)
    count += 1

def add_data_cta(html):
    """Mark primary CTA controls so analytics.js can read them."""
    def repl(match):
        tag = match.group(0)
        if re.search(r'\bdata-cta\s*=', tag, re.I):
            return tag
        classes = re.search(r'\bclass\s*=\s*"([^"]*)"', tag, re.I)
        if not classes:
            return tag
        names = set(classes.group(1).split())
        primary = (
            ('btn' in names and 'primary' in names)
            or 'pe-button' in names
            or ('oe-button' in names and 'oe-outline' not in names)
            or ('ei-btn' in names and 'alt' not in names)
        )
        if not primary:
            return tag
        return tag[:-1] + ' data-cta="primary">'

    return re.sub(r'<(?:a|button)\b[^>]*>', repl, html, flags=re.I)


CONSENT_TAG = '<script defer src="/assets/analytics-consent.js"></script>'
ANALYTICS_TAG = '<script defer src="/assets/analytics.js"></script>'
BOOT_TAG = '<script defer src="/assets/posthog-boot.js"></script>'
CONSENT_RE = re.compile(
    r'<script\s+defer\s+src="/assets/analytics-consent\.js"\s*>\s*</script>',
    re.I,
)


def inject_analytics(html):
    html = add_data_cta(html)
    if ('/assets/analytics-consent.js' in html
            and '/assets/analytics.js' in html
            and '/assets/posthog-boot.js' in html):
        return html
    if CONSENT_RE.search(html):
        def repl(match):
            extra = ''
            if '/assets/analytics.js' not in html:
                extra += ANALYTICS_TAG
            if '/assets/posthog-boot.js' not in html:
                extra += BOOT_TAG
            return match.group(0) + extra
        return CONSENT_RE.sub(repl, html, count=1)
    block = ''
    if '/assets/analytics-consent.js' not in html:
        block += CONSENT_TAG
    if '/assets/analytics.js' not in html:
        block += ANALYTICS_TAG
    if '/assets/posthog-boot.js' not in html:
        block += BOOT_TAG
    if '</head>' in html:
        return html.replace('</head>', block + '</head>', 1)
    if '</body>' in html:
        return html.replace('</body>', block + '</body>', 1)
    return html + block


def write_posthog_boot():
    template = (ROOT / "tools" / "posthog_boot_template.js").read_text(encoding="utf-8")
    boot = (template
            .replace("__POSTHOG_TOKEN__", json.dumps(POSTHOG_TOKEN))
            .replace("__POSTHOG_HOST__", json.dumps(POSTHOG_HOST))
            .replace("__POSTHOG_UI_HOST__", json.dumps(POSTHOG_UI_HOST)))
    if "__POSTHOG_" in boot:
        raise SystemExit("PostHog boot template still has unsubstituted placeholders")
    target = PUBLIC / "assets" / "posthog-boot.js"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(boot, encoding="utf-8")
    return boot


write_posthog_boot()
pages = [p for p in PUBLIC.rglob("*.html") if p.is_file()]
if not pages:
    raise SystemExit("No HTML pages in the publish directory")
for page in pages:
    text = page.read_text(encoding="utf-8")
    updated = inject_analytics(text)
    if updated != text:
        page.write_text(updated, encoding="utf-8")

boot_js = (PUBLIC / "assets" / "posthog-boot.js").read_text(encoding="utf-8")
analytics_js = (PUBLIC / "assets" / "analytics.js").read_text(encoding="utf-8")
for needle in (
    "cookieless_mode: 'always'",
    "persistence: 'memory'",
    "disable_session_recording: true",
    "autocapture: false",
    "capture_pageview: true",
    "capture_pageleave: true",
    "person_profiles: 'identified_only'",
    "respect_dnt: true",
    "-assets.i.posthog.com",
    POSTHOG_HOST,
):
    if needle not in boot_js:
        raise SystemExit("PostHog boot script missing " + needle)
if POSTHOG_TOKEN not in boot_js:
    raise SystemExit("PostHog token missing from generated boot script")
if "phc_" in analytics_js or POSTHOG_TOKEN in analytics_js:
    raise SystemExit("PostHog token must not be copied into analytics.js")
missing_scripts = []
for page in pages:
    text = page.read_text(encoding="utf-8")
    if POSTHOG_TOKEN in text:
        raise SystemExit("PostHog token was inlined into " + str(page.relative_to(PUBLIC)))
    for src in ("/assets/analytics-consent.js", "/assets/analytics.js", "/assets/posthog-boot.js"):
        if src not in text:
            missing_scripts.append(f"{page.relative_to(PUBLIC)} missing {src}")
if missing_scripts:
    raise SystemExit("Analytics scripts missing:\n" + "\n".join(missing_scripts[:20]))
if 'data-cta="primary"' not in (PUBLIC / "index.html").read_text(encoding="utf-8"):
    raise SystemExit("Homepage primary CTAs were not marked with data-cta")

required = [
    "index.html", "404.html", "sitemap.xml",
    "assets/ultrahuman-intro.js", "assets/intro-highlight-reel.css",
    "assets/adam-founder-lifestyle-branded-2026.webp",
    "assets/analytics.js", "assets/analytics-consent.js", "assets/posthog-boot.js",
    "body/index.html",
]
missing = [p for p in required if not (PUBLIC / p).is_file()]
if missing:
    raise SystemExit("Missing public files: " + ", ".join(missing))

# Guard against accidentally leaking hidden source or internal release work.
private = [
    p for p in PUBLIC.rglob("*") if p.is_file() and (
        p.suffix.lower() in {".md", ".yaml", ".yml", ".toml", ".map", ".json", ".txt", ".py", ".sh", ".patch"} and p.name != "robots.txt" or
        "docs" in p.parts or "scripts" in p.parts or
        p.name in {"package.json", "package-lock.json"}
    )
]
if private:
    raise SystemExit("Non-public files included: " + str(private[:10]))

# Do not make the retired founder photos publicly accessible.
for retired in ("founder-adam-original-formal.png", "founder-adam-original-blue-shirt.png", "founder-adam-ecoflow-event.png", "adam-founder-editorial-v3.webp"):
    if (PUBLIC / "assets" / retired).exists():
        raise SystemExit("Retired founder photograph still published: " + retired)

class LocalAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in {"img", "script", "source"}:
            href = a.get("src", "")
        elif tag == "link" and a.get("rel") in {"stylesheet", "icon"}:
            href = a.get("href", "")
        else:
            return
        if href.startswith("/"):
            self.paths.append(urlsplit(href).path)

# These critical pages must reference files present in the publish output.
for page in ["index.html", "body/index.html", "shop/index.html"]:
    parser = LocalAssets()
    parser.feed((PUBLIC / page).read_text(encoding="utf-8"))
    for asset in parser.paths:
        if asset.startswith("/api/") or asset.startswith("/.netlify/"):
            continue
        if not (PUBLIC / unquote(asset).lstrip("/")).is_file():
            raise SystemExit(f"Missing local asset in {page}: {asset}")

print(f"Prepared public-only Netlify site: {count} files, no private source files.")
