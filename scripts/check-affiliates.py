"""Guard affiliate identity, placement attribution and preview-only content."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MERCHANTS = {'69428': 'ultrahuman.com', '114180': 'sinocare.com',
             '59683': 'apebornfitness.com', '119813': 'willandbear.com',
             '96299': 'otraeyewear.com', '82371': 'aeternum.site',
             '105805': 'einstar.com'}

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
    if str(path.relative_to(ROOT)) in ('index.html', 'shop/index.html', 'products/aeternum/index.html', 'products/otra/index.html', 'products/einstar/index.html', 'articles/otra-eyewear-style-guide.html'):
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
assert len(re.findall(r'<article class="intro-slide', opening)) == 8, 'highlight reel should have eight slides'
assert 'Discover EINSTAR 3D scanning' in opening and 'href="/products/einstar/"' in opening
assert 'class="intro-video-overlay"' in opening and 'data-intro-video-close' in opening
assert '<div class="ultra-film"' not in opening, 'old auto-playing film panel returned'
assert '/assets/intro-highlight-reel.css' in home and '/assets/founder-editorial.css' in home
intro_js = (ROOT / 'assets/ultrahuman-intro.js').read_text()
assert '7600' in intro_js and 'schedule()' in intro_js and 'closeVideo()' in intro_js
# Founder imagery must be original pixels from the supplied reference archive.
opening_founder = home[home.index('id="founder-perspective"'):home.index('</section>', home.index('id="founder-perspective"'))]
original_portraits = (
    'founder-adam-original-formal.png',
    'founder-adam-original-blue-shirt.png',
    'founder-adam-ecoflow-event.png'
)
assert all(name in opening_founder for name in original_portraits), 'authentic founder photo missing'
assert 'adam-founder-editorial-v3.webp' not in opening_founder, 'illustrative founder collage is disallowed'
assert all((ROOT / 'assets' / name).is_file() for name in original_portraits)
assert '/products/einstar/' in (ROOT / 'shop/index.html').read_text(), 'EINSTAR missing from directory'
assert 'iherb' not in (ROOT / 'shop/index.html').read_text().lower(), 'iHerb must remain off public shop'
assert '/products/sinocare/' in home and '/products/ape-born/' in home and '/products/aeternum/' in home
assert 'href="https://www.ultrahuman.com/au/ring/"' not in home, 'untracked homepage buying link'
sitemap = {x.text for x in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')}
for rel in ('products/otra/index.html', 'articles/otra-eyewear-style-guide.html'):
    path = ROOT / rel; p = Page(path); p.feed(path.read_text())
    assert 'noindex' in p.robots and 'not approved for promotion' in path.read_text().lower(), (rel, 'draft guard missing')
    assert p.canonicals and all(u not in sitemap for u in p.canonicals), (rel, 'draft indexed')
for rel in ('products/ultrahuman/index.html', 'index.html'):
    text = (ROOT / rel).read_text()
    assert not re.search(r'20\s*%\s*(?:off|discount)', text, re.I), (rel, 'unconfirmed discount')
print(f'PASS: {count} affiliate links across seven partners; publisher/destinations, click references, sponsored attributes, key assets, founder and draft guards')
