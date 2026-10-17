"""Render original silent editorial reels from existing approved Youtopia imagery."""
from pathlib import Path
import subprocess,json,textwrap
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/social/journal-launch';TMP=ROOT.parent/'social-render-work';TMP.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
items=[('sleep','assets/guide-sleep.jpg','SLEEP.\nBEYOND THE SCORE.',['Sleep and biological age\nare linked in research.','An association does not tell us\nthat a bedtime reverses ageing.','Read the evidence.\nThen explore our sleep guide.']),('creatine','assets/nutrition/training-campaign.webp','CREATINE.\nBEYOND THE GYM.',['Strong exercise evidence.\nA more complicated brain story.','Promising cognitive findings\nstill need better comparisons.','Muscle. Memory. Meaningful outcomes.\nRead our full feature.']),('clocks','assets/research-watch/epigenetic-clocks.webp','A YOUNGER SCORE.\nA LONGER LIFE?',['Biological-age tests measure\nparticular signals.','Different clocks can respond\ndifferently to an intervention.','A lower score alone does not\nprove a longer, healthier life.'])]
for slug,image,title,scenes in items:
 filters=[]
 # Reframe the existing art within a new motion editorial, not fabricated study footage.
 crop='crop=816:510:0:350,' if slug=='clocks' else ''
 filters.append('[0:v]'+crop+'scale=936:650:force_original_aspect_ratio=increase,crop=936:650[photo]')
 filters.append('color=c=0xf5f3ec:s=1080x1920:r=24:d=21[paper]')
 filters.append('[paper][photo]overlay=72:545[base]')
 draw=[]
 def tx(name,text,y,size,font=FONT,color='0x111b17',enable=None):
  p=TMP/f'{slug}-{name}.txt';p.write_text(text)
  v=f"drawtext=fontfile='{font}':textfile='{p}':fontsize={size}:fontcolor={color}:x=72:y={y}:line_spacing=18"
  if enable:v+=f":enable='{enable}'"
  draw.append(v)
 tx('brand','YOUTOPIA LIFE',190,39)
 tx('kicker','THE JOURNAL  /  EVIDENCE & POSSIBILITY',263,22,color='0x467664')
 tx('title',title,350,63,SERIF)
 draw+=['drawbox=x=72:y=310:w=936:h=2:color=0x254b3c:t=fill']
 for i,scene in enumerate(scenes):tx('scene'+str(i),scene,1250,40,enable=f'between(t,{i*6},{i*6+5.99})')
 tx('finish','READ THE FULL FEATURE',1250,41,enable='gte(t,18)')
 tx('url','YOUTOPIALIFE.COM',1470,40)
 tx('follow','FOLLOW FOR THE NEXT DISCOVERY',1545,23,color='0x467664')
 tx('disclosure','AI-assisted editorial imagery. Educational reporting.',1635,19,color='0x626b65')
 draw+=['drawbox=x=72:y=1710:w=936:h=3:color=0xbcd9ca:t=fill','fade=t=in:st=0:d=0.3,fade=t=out:st=20.6:d=0.4,format=yuv420p']
 filters.append('[base]'+','.join(draw)+'[v]')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',str(ROOT/image),'-filter_complex',';'.join(filters),'-map','[v]','-t','21','-r','24','-c:v','libx264','-preset','veryfast','-crf','23','-threads','2','-an','-movflags','+faststart',str(OUT/f'{slug}-reel.mp4')],check=True)
 print(slug,flush=True)
