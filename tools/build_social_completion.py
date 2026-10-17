"""Compose new editorial layouts from approved imagery; render platform-safe motion cuts."""
from pathlib import Path
import subprocess,json,re,html,textwrap
R=Path(__file__).resolve().parents[1];O=R/'assets/social/edition-complete';O.mkdir(parents=True,exist_ok=True);T=R.parent/'social-completion-work';T.mkdir(exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';S='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
fallback={'nmn-human-evidence':'assets/guide-supplements.jpg','sleep-biological-ageing':'assets/guide-sleep.jpg','brocelite-sulforaphane':'assets/editorial-broccoli.svg','akkermansia-gut-evidence':'assets/research-watch/gut-brain.webp','memory-clarity-evidence':'assets/guide-meditation.jpg','cold-exposure-evidence':'assets/editorial-cold.svg'}
items=[]
for a in json.load(open(R/'LONG_FEATURE_AUDIT_2026-10-17.json')):
 slug=a['slug'];raw=(R/'articles'/f'{slug}.html').read_text();src=html.unescape(re.findall(r'<img[^>]+src="([^"]+)',raw)[0]);image=fallback.get(slug,src.lstrip('/'));desc=html.unescape(re.search(r'<meta name="description" content="([^"]+)',raw).group(1));items.append(dict(slug=slug,title=a['title'],image=image,description=desc,path=f'/articles/{slug}.html'))
items.append(dict(slug='night-light',title='Give the night its darkness.',image='assets/guide-circadian.jpg',description='Light is a timing signal. Explore the evidence behind morning light, evening routines and a more consistent body clock.',path='/guides/circadian-rhythm.html'))
manifest=[]
for a in items:
 if a['slug'] in {'brocelite-sulforaphane','cold-exposure-evidence'}:continue
 slug=a['slug'];isposter='/research-watch/' in a['image'];filters=[]
 crop=('crop=816:510:0:350,' if slug=='research-watch-epigenetic-clocks' else 'crop=iw:ih*0.27:0:ih*0.23,') if isposter else ''
 filters.append('[0:v]'+crop+'scale=936:680:force_original_aspect_ratio=increase,crop=936:680[photo]');filters.append('color=c=0xf5f3ec:s=1080x1920:r=24:d=12[paper]');filters.append('[paper][photo]overlay=72:565[base]');draw=[]
 def tx(n,text,y,size,font=F,color='0x14261e'):
  p=T/f'{slug}-{n}.txt';p.write_text(text);draw.append(f"drawtext=fontfile='{font}':textfile='{p}':fontsize={size}:fontcolor={color}:x=72:y={y}:line_spacing=12")
 tx('brand','YOUTOPIA LIFE',190,39);tx('kicker','THE JOURNAL  /  EVIDENCE & POSSIBILITY',260,22,color='0x467664');draw.append('drawbox=x=72:y=310:w=936:h=2:color=0x254b3c:t=fill')
 title=textwrap.fill(a['title'],30);tx('title',title,355,48,S);tx('dek',textwrap.fill(a['description'],58),1300,26);tx('read','READ THE FULL FEATURE',1530,26);tx('site','FOLLOW YOUTOPIALIFE.COM',1590,36);tx('foot','AI-assisted editorial imagery. Educational reporting.',1680,19,color='0x626b65');draw.append('drawbox=x=72:y=1730:w=936:h=3:color=0xbcd9ca:t=fill')
 filters.append('[base]'+','.join(draw)+',format=yuv420p[v]')
 cmd=['ffmpeg','-y','-loglevel','error','-i',str(R/a['image']),'-filter_complex',';'.join(filters),'-map','[v]','-frames:v','1','-threads','2',str(O/f'{slug}-story.jpg')];subprocess.run(cmd,check=True)
 # Full vertical layout retains a website CTA and stays inside Story safe areas.
 a['story']=f'assets/social/edition-complete/{slug}-story.jpg'
 a['post']=a['story']
 if slug in ['night-light','research-watch-protein-clocks','research-watch-living-brain','sleep-biological-ageing','creatine-body-brain','research-watch-epigenetic-clocks']:
  subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',str(O/f'{slug}-story.jpg'),'-vf','fade=t=in:st=0:d=0.35,fade=t=out:st=11.6:d=0.4,format=yuv420p','-t','12','-r','24','-c:v','libx264','-preset','veryfast','-crf','23','-threads','2','-an','-movflags','+faststart',str(O/f'{slug}-story.mp4')],check=True)
  a['video']=f'assets/social/edition-complete/{slug}-story.mp4'
 manifest.append(a);print(slug,flush=True)
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
