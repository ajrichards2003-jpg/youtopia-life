"""Static smoke checks for the homepage. No external dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]

class HomeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.ids = set()
        self.forms = []
        self.current_form = None
        self.inputs = []
        self.newsletter_count = 0
        self.images = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'img':
            self.images += 1
        if tag in ('img', 'script', 'source', 'link'):
            for key in ('src', 'href', 'srcset'):
                if key in a and a[key] and key != 'srcset':
                    self.assets.append((tag, a[key]))
        if tag == 'form':
            self.current_form = a.get('name')
            if self.current_form == 'youtopia-weekly':
                self.newsletter_count += 1
        if tag == 'input' and self.current_form == 'youtopia-weekly':
            self.inputs.append(a)

    def handle_endtag(self, tag):
        if tag == 'form':
            self.current_form = None

p = HomeParser()
p.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
missing = []
for tag, ref in p.assets:
    if not ref.startswith('/') or ref.startswith('//'):
        continue
    path = unquote(urlsplit(ref).path).lstrip('/')
    if not path or path.endswith('/'):
        continue
    if not (ROOT / path).is_file():
        missing.append((tag, ref))

assert p.newsletter_count == 1, f'Expected one newsletter form, found {p.newsletter_count}'
assert any(x.get('name') == 'email' and x.get('type') == 'email' and 'required' in x for x in p.inputs), 'Newsletter email required field missing'
assert any(x.get('name') == 'weekly-consent' and 'required' in x for x in p.inputs), 'Newsletter consent missing'
assert 'weekly' in p.ids and 'frontier' in p.ids, 'Core homepage sections missing'
assert not missing, 'Missing local homepage assets: ' + repr(missing)
print(f'PASS: {p.images} images, {len(p.assets)} asset references, newsletter and key sections validated')
