"""Check canonical discovery and structured data against the actual journal HTML."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,xml.etree.ElementTree as ET,tomllib
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.meta={};self.canonical=[];self.json=[];self.buffer=None;self.title='';self.in_title=False;self.breadcrumb=False;self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='script' and a.get('type')=='application/ld+json':self.buffer=''
  if tag=='title':self.in_title=True
  if tag=='nav' and a.get('aria-label')=='Breadcrumb':self.breadcrumb=True
  if tag=='a':self.links.append(a.get('href'))
 def handle_data(self,s):
  if self.buffer is not None:self.buffer+=s
  if self.in_title:self.title+=s
 def handle_endtag(self,tag):
  if tag=='script' and self.buffer is not None:self.json.append(json.loads(self.buffer));self.buffer=None
  if tag=='title':self.in_title=False
sitemap=ET.parse(ROOT/'sitemap.xml');urls=[x.text for x in sitemap.findall('.//{*}loc')]
redirects=tomllib.loads((ROOT/'netlify.toml').read_text())['redirects'];titles=[]
for p in sorted((ROOT/'articles').glob('*.html')):
 if p.stem=='index':continue
 if re.search(r'<meta name="robots" content="noindex', p.read_text()):continue
 d=Page();d.feed(p.read_text());url='https://youtopialife.com/articles/'+p.name
 assert d.canonical==[url],(p.name,'canonical')
 assert urls.count(url)==1 and url.removesuffix('.html') not in urls,(p.name,'sitemap mismatch')
 assert d.breadcrumb and '/editorial/#editorial-team' in d.links,(p.name,'visible attribution/breadcrumb')
 assert d.meta['robots']=='index,follow,max-image-preview:large'
 assert d.meta['description'] and d.meta['twitter:image'] and d.meta['og:url']==url
 graph=d.json[0]['@graph'];article=next(x for x in graph if x['@type']=='Article');bread=next(x for x in graph if x['@type']=='BreadcrumbList')
 assert article['url']==article['mainEntityOfPage']==url
 assert all(u in d.links for u in article['citation']) and len(article['citation'])>=3
 assert article['author']['@id']=='https://youtopialife.com/editorial/#editorial-team'
 assert 1500<=article['wordCount']<=3000 and bread['itemListElement'][-1]['item']==url
 assert any(x['from']=='/articles/'+p.stem and x['to']=='/articles/'+p.name and x['status']==301 for x in redirects)
 titles.append(d.title)
assert len(titles)==20 and len(set(titles))==20
print('PASS: 20 unique search titles; canonical URLs, sitemap, redirects, visible attribution, citations and schema agree')
