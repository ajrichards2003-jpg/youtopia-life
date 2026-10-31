"""Guard sitemap, canonical and retired URL consistency before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import tomllib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://youtopialife.com"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.canonical, self.robots, self.links = [], [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical.append(attrs.get("href"))
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots.append(attrs.get("content", "").lower())
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])


def resolve(path):
    file = ROOT / unquote(path).lstrip("/")
    return next((p for p in (file, file / "index.html", Path(str(file) + ".html"))
                 if p.is_file()), None)


rules = tomllib.loads((ROOT / "netlify.toml").read_text())["redirects"]
redirects = {r["from"]: r for r in rules if "*" not in r["from"]}
assert len(redirects) == sum("*" not in r["from"] for r in rules), "Repeated redirect source"
urls = [node.text for node in ET.parse(ROOT / "sitemap.xml").findall(".//{*}loc")]
assert len(urls) == len(set(urls)), "Repeated sitemap URL"
for url in urls:
    parsed = urlsplit(url)
    assert parsed.scheme == "https" and parsed.netloc == "youtopialife.com", url
    assert parsed.path not in redirects, (url, "redirect in sitemap")
    file = resolve(parsed.path)
    assert file, (url, "missing sitemap destination")
    page = Page(file)
    assert page.canonical == [url], (url, "canonical mismatch", page.canonical)
    assert not any("noindex" in r for r in page.robots), (url, "noindex in sitemap")

retired = {
    "/product-policy": "/editorial/",
    "/articles/01-essential-supplement-stack": "/supplements/",
    "/articles/02-red-light-sauna-cold-plunge": "/articles/red-light-evidence.html",
    "/articles/03-meditation-20-minutes": "/guides/meditation.html",
    "/articles/04-peptides-spotlight": "/peptides/",
}
for old, target in retired.items():
    for source in (old, old + ".html"):
        rule = redirects[source]
        assert rule["to"] == target and rule["status"] == 301 and rule.get("force"), source
        assert ORIGIN + target in urls, (source, "target is not canonical/indexable")

assert redirects["/books.html"]["to"] == "/books"
for source, rule in redirects.items():
    if rule["status"] != 301:
        continue
    seen = {source}
    target = rule["to"]
    while target in redirects:
        assert target not in seen, (source, "redirect loop")
        seen.add(target)
        target = redirects[target]["to"]
    assert resolve(target), (source, "missing redirect destination", target)

for file in ROOT.rglob("*.html"):
    page = Page(file)
    for href in page.links:
        url = urlsplit(urljoin(ORIGIN + "/" + str(file.relative_to(ROOT)), href))
        if url.netloc != "youtopialife.com":
            continue
        assert resolve(url.path) or url.path in redirects, (str(file), href, "broken internal link")

for path in ("body/index.html", "store/index.html", "contact/thanks/index.html",
             "newsletter/thanks/index.html", "store/thanks/index.html", "store/thanks.html"):
    assert any("noindex" in value for value in Page(ROOT / path).robots), path

print(f"PASS: {len(urls)} canonical/indexable sitemap URLs; ten legacy URL forms; "
      "redirect destinations/loops; internal page links; intentional noindex pages")
