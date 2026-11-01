"""Guard affiliate identity, placement attribution and preview-only content."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MERCHANTS = {'69428': 'ultrahuman.com'}  # Ledger register 1 Nov: only confirmed partner
GATED = ('products/otra/', 'products/aeternum/', 'products/einstar/', 'products/ape-born/', 'products/sinocare/',
         'articles/sinocare-home-monitoring.html', 'articles/ape-born-muscle-stimulation.html', 'articles/otra-eyewear-style-guide.html')

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path = path; self.links = []; self.ids = []
        self.assets = []; self.robots = ''; self.canonicals = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'a': self.links.append(a)
        if tag == 'meta' and a.get('name') == 'robots': self.robots = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a['href'])
        if tag == 'img': self.assets.append(a.get('src', ''))
        if tag == 'link' and a.get('rel') == 'stylesheet': self.assets.append(a.get('href', ''))

count = 0
seen = set()
for path in ROOT.rglob('*.html'):
    if path.relative_to(ROOT).as_posix().startswith(GATED + ('public-site/',)): continue
    p = Page(path); p.feed(path.read_text())
    for a in p.links:
        u = urlsplit(a.get('href', ''))
        if u.netloc not in ('www.awin1.com', 'awin1.com'): continue
        q = parse_qs(u.query)
        assert q.get('awinaffid') == ['3106417'], (path, 'wrong publisher')
        mid = q.get('awinmid', [''])[0]
        assert mid in MERCHANTS, (path, 'unknown merchant', mid)
        dest = urlsplit(q.get('ued', [''])[0])
        assert dest.scheme == 'https' and (dest.netloc == MERCHANTS[mid] or dest.netloc.endswith('.' + MERCHANTS[mid])), (path, 'merchant/destination mismatch')
        assert q.get('clickref') and 'sponsored' in a.get('rel', '').split(), (path, 'missing attribution/disclosure attribute')
        seen.add(mid); count += 1
    if str(path.relative_to(ROOT)) in ('index.html', 'shop/index.html', 'products/ultrahuman/index.html'):
        assert len(p.ids) == len(set(p.ids)), (path, 'duplicate ID')
        for asset in p.assets:
            u = urlsplit(asset)
            if u.path.startswith('/') and not u.netloc:
                assert (ROOT / u.path.lstrip('/')).is_file(), (path, asset)
        for a in p.links:
            u = urlsplit(a.get('href', ''))
            if not u.path and u.fragment: assert u.fragment in p.ids, (path, 'missing fragment', u.fragment)

assert seen == set(MERCHANTS), ('partner missing', seen)
home = (ROOT / 'index.html').read_text()
opening = home[home.index('<section class="intro-carousel ultra-intro"'):home.index('</section>', home.index('<section class="intro-carousel ultra-intro"'))]
# A user-controlled highlights reel replaces the old intrusive Ultrahuman film takeover.
assert 'class="intro-pause"' in opening and 'class="intro-replay"' not in opening
assert 'data-intro-video="-sDcFyZLxTY"' in opening, 'dire wolf film missing'
assert len(re.findall(r'<article class="intro-slide', opening)) == 5, 'highlight reel should have five slides'
assert 'class="intro-video-overlay"' in opening and 'data-intro-video-close' in opening
assert '<div class="ultra-film"' not in opening, 'old auto-playing film panel returned'
assert '/assets/intro-highlight-reel.css' in home and '/assets/founder-editorial.css' in home
intro_js = (ROOT / 'assets/ultrahuman-intro.js').read_text()
assert '7600' in intro_js and 'schedule()' in intro_js and 'closeVideo()' in intro_js
# The founder-approved brand editorial replaces the old photo tiles.
opening_founder = home[home.index('id="founder-perspective"'):home.index('</section>', home.index('id="founder-perspective"'))]
approved_asset = 'adam-founder-lifestyle-branded-2026.webp'
assert approved_asset in opening_founder, 'approved Youtopia lifestyle artwork missing'
assert (ROOT / 'assets' / approved_asset).is_file(), 'approved lifestyle artwork asset not present'
assert 'AI-assisted lifestyle editorial' in opening_founder, 'artwork must be described as a brand concept'
assert 'Adam Richards' in opening_founder and 'Youtopia Life' in opening_founder
for stale in ('founder-adam-original-formal.png', 'founder-adam-original-blue-shirt.png', 'founder-adam-ecoflow-event.png', 'adam-founder-editorial-v3.webp'):
    assert stale not in opening_founder, ('old founder image still in feature', stale)
assert 'iherb' not in (ROOT / 'shop/index.html').read_text().lower(), 'iHerb must remain off public shop'
for page in ('index.html', 'shop/index.html', 'wearables/index.html', 'articles/index.html'):
    t = (ROOT / page).read_text()
    for g in ('/products/sinocare/', '/products/ape-born/', '/products/aeternum/', '/products/otra/', '/products/einstar/', 'willandbear'):
        assert g not in t, (page, 'unconfirmed partner linked', g)
assert 'href="https://www.ultrahuman.com/au/ring/"' not in home, 'untracked homepage buying link'
sitemap = {x.text for x in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')}
for g in GATED:
    assert all(g not in u for u in sitemap), (g, 'gated page in sitemap')
for rel in ('products/ultrahuman/index.html', 'index.html'):
    text = (ROOT / rel).read_text()
    assert not re.search(r'20\s*%\s*(?:off|discount)', text, re.I), (rel, 'unconfirmed discount')
print(f'PASS: {count} affiliate links (Ultrahuman only); publisher/destinations, click references, sponsored attributes, key assets, founder and draft guards')
