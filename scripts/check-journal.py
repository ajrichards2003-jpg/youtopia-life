"""Validate the editorial feature contract without counting surrounding page furniture."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re,json

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED_CLASSES={'pullquote','sources','note','back-top','film'}
class Feature(HTMLParser):
    def __init__(self):
        super().__init__();self.stack=[];self.story=[];self.links=[];self.ids=[];self.h1=0;self.inside=False;self.depth=0;self.excluded=0;self.sources=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='main' and a.get('id')=='story':self.inside=True;self.depth=0
        excluded=self.inside and (bool(set(a.get('class','').split())&EXCLUDED_CLASSES) or a.get('id')=='sources')
        if self.inside:
            self.depth+=1
            if excluded:self.excluded+=1
        self.stack.append((tag,excluded,self.inside)) if tag not in {'img','meta','link','br','hr','source','input','wbr'} else None
        if tag=='a' and a.get('href','').startswith('https://') and self.excluded:self.sources+=1
        for key in ('href','src','poster'):
            if a.get(key):self.links.append(a[key])
    def handle_endtag(self,tag):
        if self.stack and self.stack[-1][0]==tag:
            _,excluded,wasinside=self.stack.pop()
            if excluded:self.excluded-=1
        if tag=='main':self.inside=False
    def handle_data(self,text):
        if self.inside and self.excluded==0:self.story.append(text)

counts=[]
for path in sorted((ROOT/'articles').glob('*.html')):
    if path.name=='index.html':continue
    f=Feature();f.feed(path.read_text(encoding='utf-8'))
    count=len(re.findall(r"\b[\w]+(?:[’'–-][\w]+)*\b",' '.join(f.story)))
    assert 1500<=count<=3000,(path.name,count)
    assert f.h1==1,(path.name,'main heading count')
    assert len(f.ids)==len(set(f.ids)),(path.name,'duplicate IDs')
    assert f.sources>=3,(path.name,'source trail missing')
    for ref in f.links:
        u=urlsplit(ref)
        if not u.scheme and not u.netloc and u.path.startswith('/'):
            dest=ROOT/unquote(u.path.lstrip('/'))
            assert dest.exists() or dest.with_suffix('.html').exists(),(path.name,ref)
        if not u.path and u.fragment:assert u.fragment in f.ids,(path.name,ref)
    counts.append((path.stem,count))
assert len(counts)==20,('Expected 20 feature articles',len(counts))
print('PASS: 20 features; story words',min(n for _,n in counts),'to',max(n for _,n in counts),'; headings, sources, IDs and local links valid')
for slug,count in counts:print(f'{count:4d} {slug}')
