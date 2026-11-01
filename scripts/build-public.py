#!/usr/bin/env python3
"""Copy only public website files into Netlify's publish directory.

Do not deploy the repository root: it also contains private planning material,
scripts, PR notes, package manifests and internal QA documents.
"""
from pathlib import Path
from shutil import copy2, rmtree
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public-site"

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
    target = PUBLIC / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, target)
    count += 1

required = [
    "index.html", "404.html", "sitemap.xml",
    "assets/ultrahuman-intro.js", "assets/intro-highlight-reel.css",
    "assets/adam-founder-lifestyle-branded-2026.webp",
    "products/einstar/index.html", "body/index.html",
]
missing = [p for p in required if not (PUBLIC / p).is_file()]
if missing:
    raise SystemExit("Missing public files: " + ", ".join(missing))

# Guard against accidentally leaking hidden source or internal release work.
private = [
    p for p in PUBLIC.rglob("*") if p.is_file() and (
        p.suffix.lower() in {".md", ".yaml", ".yml", ".toml", ".map"} or
        "docs" in p.parts or "scripts" in p.parts or
        p.name in {"package.json", "package-lock.json"}
    )
]
if private:
    raise SystemExit("Non-public files included: " + str(private[:10]))

# Do not make the retired founder photos publicly accessible.
for retired in ("founder-adam-original-formal.png", "founder-adam-original-blue-shirt.png", "founder-adam-ecoflow-event.png"):
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
for page in ["index.html", "body/index.html", "shop/index.html", "products/einstar/index.html"]:
    parser = LocalAssets()
    parser.feed((PUBLIC / page).read_text(encoding="utf-8"))
    for asset in parser.paths:
        if asset.startswith("/api/") or asset.startswith("/.netlify/"):
            continue
        if not (PUBLIC / unquote(asset).lstrip("/")).is_file():
            raise SystemExit(f"Missing local asset in {page}: {asset}")

print(f"Prepared public-only Netlify site: {count} files, no private source files.")
