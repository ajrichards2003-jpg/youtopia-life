"""Free, reproducible Ring AIR campaign edit and fourteen-day social pack.

Artwork is a campaign visualisation pending advertiser approval. No AI video
subscription, external music, customer testimonial or invented app screen.
"""
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json, csv, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / 'output' / 'youtopia-campaign'
OUT.mkdir(parents=True, exist_ok=True)
BG=(3,16,13); MINT=(80,224,185); WHITE=(243,244,232); MUTED=(178,200,190)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
AFF='https://www.awin1.com/cread.php?awinmid=69428&awinaffid=3106417&ued=https%3A%2F%2Fwww.ultrahuman.com%2Fau%2Fring%2Fbuy%2F'
TZ=ZoneInfo('Australia/Sydney')

PRODUCTS=[
('hero','SMALL RING.\nBIGGER PICTURE.','Sleep. Heart-rate trends. Everyday movement.','Meet Ring AIR: a compact wearable that puts sleep, heart-rate and movement insights in one place. Our 30-second launch film introduces the questions it can help you explore. Which would you track first: sleep, recovery or activity?','video'),
('sleep','YOUR NIGHT.\nIN FOCUS.','Sleep duration and estimated stages.','Eight hours in bed and eight hours asleep are different questions. Ring AIR tracks sleep duration and estimates stages so you can explore your overnight patterns. What would you most like to understand about your nights?','image'),
('heart','FOLLOW YOUR\nHEART.','Resting heart rate and HRV trends.','Your heart-rate patterns are more useful with context. Ring AIR tracks resting heart rate and heart-rate variability, which the app uses alongside other signals for recovery insights. Look for your own trends rather than chasing someone else’s number.','video'),
('activity','EVERYDAY\nMOVEMENT.','Steps and daily activity patterns.','The walk to the station. The stairs. The afternoon stroll. Ring AIR tracks steps and everyday movement, helping you see the activity that happens between workouts. What is your favourite way to move without calling it exercise?','image'),
('design','LESS BULK.\nMORE INSIGHT.','Lightweight titanium. Screen-free design.','A compact titanium ring, a screen-free design and insights in the phone app. Ring AIR takes a different approach to daily tracking. Check sizing and phone compatibility before choosing yours. Would you prefer a ring or a watch?','video'),
('sleep','SPOT THE\nPATTERN.','Compare nights, not just one score.','One unusual night is a starting point for curiosity. Compare sleep duration and estimated stages across several nights and ask what changed in your routine. Ring AIR provides estimates and trends, not a sleep diagnosis.','image'),
('design','CORE DATA.\nNO MONTHLY FEE.','Optional extras may cost more.','Ring AIR has no mandatory subscription for core ring data. Optional PowerPlugs, coverage and accessories can add cost, so compare the complete checkout total. That detail matters when choosing a wearable for the long term.','video'),
('heart','RECOVERY\nWITH CONTEXT.','Heart rate, HRV and skin-temperature trends.','How do you feel today—and what do your overnight patterns show? Ring AIR combines heart-rate, HRV and skin-temperature trends in its recovery insights. Use that context alongside how you feel; one score is not the whole story.','image'),
('hero','FIT COMES\nFIRST.','Check the official sizing guidance.','Before the colour choice comes the fit. Read Ultrahuman’s current sizing guidance and check phone compatibility, returns and delivery to Australia. A great-looking wearable should also be the right purchase for you.','video'),
('activity','MOVE. REST.\nREPEAT.','Explore activity alongside sleep.','Activity and rest belong in the same conversation. Ring AIR lets you explore daily movement alongside sleep and recovery insights. Choose one habit you would like to understand, then follow its pattern.','image'),
('hero','KNOW WHAT\nIT MEASURES.','Ring AIR does not measure glucose.','Clear expectations make better purchases. Ring AIR tracks sleep, heart-rate and movement-related signals. It does not measure blood glucose; Ultrahuman’s glucose products are separate. Start with the feature you actually need.','video'),
('design','CHECK THE\nWHOLE COST.','Fit. Extras. Delivery. Returns.','Look beyond the product photo: check the AUD total, sizing, phone compatibility, optional extras, delivery and return conditions. Ultrahuman handles your payment and fulfilment. Youtopia earns a commission only on qualifying referrals.','image'),
('sleep','YOUR ROUTINE.\nYOUR INSIGHTS.','One question. A pattern to explore.','What would you like to learn about your routine: your nights, your daily movement or your recovery patterns? Ring AIR offers a place to begin exploring. No wearable replaces your own experience or professional care.','video'),
('hero','CHOOSE WITH\nCONFIDENCE.','Explore Ring AIR at the official store.','Two weeks of Ring AIR questions—and one final thought: buy for the insights you will actually use. Check the official features and Australian purchase details before deciding. What question should we explore next?','image'),
]

EDITORIAL=[
('guide-circadian.jpg','YOUR MORNING.\nYOUR MOMENT.','A small ritual worth making yours.','Tomorrow morning, give yourself a moment before the rush: step outside, notice the day and choose one intention. We are exploring the routines that make everyday life feel more considered. What is one morning habit you enjoy?','/guides/circadian-rhythm.html','image'),
('wallpaper-1.jpg','CURIOSITY\nWITH A FILTER.','Useful. Interesting. Or just hype?','What are we watching at Youtopia? Longevity research, recovery technology, meditation, nutrition and the ideas that challenge how we think about human potential. Our filter stays simple: what does the evidence show, what remains uncertain, and what is worth exploring next?','/','image'),
('guide-supplements.jpg','READ THE\nLABEL FIRST.','Ingredient. Amount. Context.','A supplement shelf can be overwhelming. Start with the ingredient, the amount per serving and the question you are trying to answer. We have shortlisted iHerb as our next catalogue to investigate; no partnership or product endorsement is announced yet. Which category should we compare first?','/supplements/','video'),
('wallpaper-3.jpg','DISCOVER.\nTHEN VERIFY.','Ideas from The Human Upgrade and beyond.','Dave Asprey’s Human Upgrade is one of the places we discover interesting ideas. Discovery is the beginning: we then look for original research, its limits and the context behind the claim. Who would you like us to explore next?','/','image'),
('guide-meditation.jpg','A MOMENT\nTO RESET.','Pause the scroll. Find your space.','Your feed can wait for a moment. Get comfortable, relax your shoulders and notice a few natural breaths. No challenge, no score—just a pause. What helps you create a quieter moment in a busy day?','/guides/meditation.html','video'),
('guide-workout.jpg','MAKE ROOM\nFOR MOVEMENT.','Your version of an active day.','A walk with a friend. Dancing in the kitchen. A game with the kids. Movement has plenty of forms, and the one you enjoy is worth making room for. Tell us your favourite way to make an ordinary day more active.','/guides/15-minute-workout.html','image'),
('pick-sauna.jpg','HEAT. REST.\nGOOD QUESTIONS.','Explore the evidence behind recovery.','Sauna belongs in a thoughtful recovery conversation. Before copying a protocol, ask about the evidence, who it was studied in, suitability and practical safety. We are interested in the mechanics as much as the marketing. What recovery topic should we investigate next?','/','image'),
('wallpaper-2.jpg','YOUR BODY.\nCONNECTED.','Body Explorer is a work in progress.','Imagine following sugar from a meal through digestion, absorption and the body’s signalling systems—or selecting an organ to understand what it does and what it connects to. That is the direction we are developing for Body Explorer. It remains a work in progress while we get the educational experience right.','/','video'),
('guide-supplements.jpg','LESS HYPE.\nBETTER QUESTIONS.','Supplement comparisons are coming.','Our next product range will begin with questions: what is in it, what is the evidence, how does the label compare, and is it available to Australian customers? We are investigating iHerb’s range before selecting any products. Help shape the shortlist: what do you find hardest to compare?','/supplements/','image'),
('kids-family.jpg','HEALTHSPAN\nWITH COMPANY.','More life in the moments we share.','Youtopia is about more than collecting health numbers. It is about curiosity, community and making room for meaningful experiences. Call a friend, plan a family walk or share something you have learned. What does a good day look like to you?','/','image'),
('guide-eyes.jpg','LOOK UP.\nLOOK FURTHER.','Take curiosity beyond the feed.','Today’s invitation: look up from the feed and notice something you normally miss. A view, a conversation, a new question. We are building Youtopia for people who want to keep discovering. What caught your attention this week?','/','video'),
('wallpaper-4.jpg','THE FUTURE\nNEEDS QUESTIONS.','Technology with a human purpose.','New technology is exciting. The useful questions are just as exciting: what problem does it solve, who benefits, what has actually been demonstrated, and what remains a promise? That is how we want to explore AI and future health technology at Youtopia.','/','image'),
('guide-circadian.jpg','ONE HABIT.\nONE WEEK.','Start with something realistic.','You do not need a perfect routine to begin. Choose one realistic habit for the week ahead: a regular walk, a calmer evening or time to cook something you enjoy. What would make the biggest difference to your everyday experience?','/guides/circadian-rhythm.html','image'),
('wallpaper-1.jpg','WHAT SHOULD\nWE EXPLORE NEXT?','You help shape Youtopia.','Sleep, nutrition, longevity, recovery or the next leap in technology? We are building a discovery community, and your questions help shape what comes next. Leave one topic you would love explained clearly—with the mechanics, evidence and uncertainties included.','/','video'),
]

def wrap(text,font,width):
    lines=[]
    for para in text.split('\n'):
        cur=''
        for word in para.split():
            trial=(cur+' '+word).strip()
            if font.getlength(trial)>width and cur: lines.append(cur); cur=word
            else: cur=trial
        lines.append(cur)
    return lines

def card(photo,title,sub,series,n,product=False):
    im=Image.new('RGB',(1080,1350),BG); d=ImageDraw.Draw(im)
    pic=Image.open(photo).convert('RGB'); pic=ImageOps.fit(pic,(1080,660),centering=(.7,.5)); im.paste(pic,(0,115))
    # Exact editable typography is rendered separately from the source artwork.
    d=ImageDraw.Draw(im);d.rectangle((64,78,111,83),fill=MINT)
    d.text((133,53),'YOUTOPIA LIFE',font=ImageFont.truetype(BOLD,31),fill=WHITE)
    d.text((850,56),f'{n:02d} / 14',font=ImageFont.truetype(FONT,23),fill=MUTED)
    d.text((65,819),series.upper(),font=ImageFont.truetype(BOLD,23),fill=MINT)
    f=ImageFont.truetype(BOLD,70)
    y=867
    for line in wrap(title,f,940):d.text((60,y),line,font=f,fill=WHITE);y+=83
    for line in wrap(sub,ImageFont.truetype(FONT,31),930):d.text((64,y+25),line,font=ImageFont.truetype(FONT,31),fill=MUTED);y+=43
    d.line((64,1231,1016,1231),fill=(38,74,61),width=2)
    footer='Affiliate ad · Qualifying purchases may earn us commission.' if product else 'Limitless Youth · youtopialife.com'
    d.text((64,1264),footer,font=ImageFont.truetype(FONT,22),fill=MUTED)
    return im

def score():
    sr=48000;length=30;t=np.arange(sr*length)/sr;x=np.zeros(len(t))
    # Original restrained 100-bpm electronic score; no sampled commercial music.
    chords=[(110,164.81,220,261.63),(87.31,130.81,174.61,220),(98,146.83,196,246.94),(110,164.81,220,261.63),(87.31,130.81,174.61,220)]
    for k,ch in enumerate(chords):
        a=k*6;b=(k+1)*6;u=t[a*sr:b*sr]-a;env=np.minimum(u/.8,1)*np.minimum((6-u)/.8,1)
        for f in ch:x[a*sr:b*sr]+=.055*env*(np.sin(2*np.pi*f*u)+.25*np.sin(2*np.pi*f*2*u))
    rng=np.random.default_rng(14)
    for start in np.arange(0,29.5,.6):
        j=int(start*sr);u=np.arange(int(.28*sr))/sr
        kick=.26*np.exp(-u*20)*np.sin(2*np.pi*(45*u+2.0*(1-np.exp(-u*15))))
        x[j:j+len(u)]+=kick
        j+=int(.3*sr);u=np.arange(int(.07*sr))/sr;h=rng.normal(0,1,len(u));h=np.diff(h,prepend=0)*np.exp(-u*90)*.023;x[j:j+len(u)]+=h
    x*=np.minimum(t/1.1,1)*np.minimum((30-t)/1.7,1);x=x/(max(abs(x))+.01)*.72
    with wave.open(str(OUT/'original-score.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.repeat((x*32767).astype('<i2')[:,None],2,axis=1).tobytes())

def render(photo,title,sub,path,duration=6,social=True,label='RING AIR',product=True,quiet=False):
    W,H=(1080,1350) if social else (1920,1080)
    frames=int(duration*30)
    if social:
        imagefilter=f"scale=1188:-1,zoompan=z='1.0+0.025*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1080x608:fps=30,pad=1080:1350:0:180:color=0x03100d"
        titlexy=(60,880);fs=66;linegap=80;subxy=(64,1085);subfs=30
    else:
        imagefilter=f"scale=2090:-1,zoompan=z='1.0+0.045*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1920x1080:fps=30"
        imagefilter+=',drawbox=x=0:y=0:w=950:h=ih:color=0x03100d@0.18:t=fill'
        titlexy=(90,440);fs=88;linegap=103;subxy=(94,720);subfs=32
    filters=[imagefilter]
    def txt(text,x,y,size,color='0xf3f4e8',bold=False,animated=False):
        textfile=OUT/(path.stem+f'-text-{len(filters)}.txt');textfile.write_text(text)
        alpha="min(1,max(0,(t-0.25)/0.55))" if animated else '1'
        filters.append(f"drawtext=fontfile='{BOLD if bold else FONT}':textfile='{textfile}':fontsize={size}:fontcolor={color}:x={x}:y={y}:alpha='{alpha}'")
    txt('YOUTOPIA LIFE',64 if social else 94,64 if social else 73,30 if social else 27,bold=True)
    txt(label.upper(),64 if social else 94,805 if social else 364,22 if social else 25,'0x50e0b9',True)
    for i,line in enumerate(title.split('\n')):txt(line,titlexy[0],titlexy[1]+i*linegap,fs,'0x50e0b9' if i else '0xf3f4e8',True,True)
    for i,line in enumerate(wrap(sub,ImageFont.truetype(FONT,subfs),940 if social else 785)):txt(line,subxy[0],subxy[1]+i*42,subfs,'0xb2c8be',False,True)
    txt('Explore at youtopialife.com',64 if social else 94,1205 if social else 915,25 if social else 26)
    foot='Affiliate ad · Qualifying purchases may earn us commission.' if product else 'Limitless Youth · Discover with Youtopia'
    txt(foot,64 if social else 94,1283 if social else 1004,20 if social else 22,'0xb2c8be')
    filters.append('fade=t=in:st=0:d=0.25,fade=t=out:st='+str(duration-.25)+':d=0.25,format=yuv420p')
    cmd=['ffmpeg','-y','-loglevel','error','-threads','2','-i',str(photo),'-vf',','.join(filters),'-frames:v',str(frames),'-c:v','libx264','-preset','fast','-crf','19','-threads','2','-an',str(path)]
    subprocess.run(cmd,check=True)

def main():
    score(); posts=[]
    for i,p in enumerate(PRODUCTS):
        theme,title,sub,caption,media=p; day=(datetime(2026,10,4)+timedelta(days=i)).date();photo=ROOT/'assets'/'ultrahuman'/f'{theme}-campaign.webp'
        filename=f'{day}-AM-ring-{theme}.jpg';card(photo,title,sub,'Ultrahuman Ring AIR',i+1,True).save(OUT/filename,quality=94)
        if media=='video':
            video=OUT/f'{day}-AM-ring-{theme}.mp4'
            if i:render(photo,title,sub,video,12,True,'Ultrahuman Ring AIR',True)
            filename=video.name
        posts.append(dict(date=day.isoformat(),time='10:00',timezone='Australia/Sydney',slot='AM',topic=title.replace('\n',' '),format=media,filename=filename,status='DRAFT — advertiser approval required',caption='Affiliate ad · Youtopia Life may earn a commission on qualifying purchases.\n\n'+caption+'\n\nExplore Ring AIR at Ultrahuman: '+AFF+'\n\nFeatures are wellness insights, not medical diagnoses. Campaign visuals are AI-assisted. #YoutopiaAustralia #Ultrahuman #RingAIR'))
        photo_name,title,sub,caption,link,media=EDITORIAL[i]; filename=f'{day}-PM-youtopia.jpg';card(ROOT/'assets'/photo_name,title,sub,'The Youtopia daily discovery',i+1).save(OUT/filename,quality=94)
        if media=='video':
            video=OUT/f'{day}-PM-youtopia.mp4';render(ROOT/'assets'/photo_name,title,sub,video,10,True,'Daily discovery',False);filename=video.name
        posts.append(dict(date=day.isoformat(),time='17:30',timezone='Australia/Sydney',slot='PM',topic=title.replace('\n',' '),format=media,filename=filename,status='READY TO SCHEDULE',caption=caption+'\n\nExplore: https://youtopialife.com'+link+'?utm_source=facebook&utm_medium=organic_social&utm_campaign=october_discovery&utm_content=d'+str(i+1)+'\n\n#YoutopiaAustralia #YoutopiaLife #LimitlessYouth'))
    # Five six-second scenes, precisely thirty seconds in both delivery formats.
    for social in (False,True):
        scenes=[]
        for i,theme in enumerate(('hero','sleep','heart','activity','design')):
            p=PRODUCTS[i];path=OUT/f'master-{social}-scene{i}.mp4';render(ROOT/'assets'/'ultrahuman'/f'{theme}-campaign.webp',p[1],p[2],path,6,social,'Ultrahuman Ring AIR',True);scenes.append(path)
        listing=OUT/f'concat-{social}.txt';listing.write_text('\n'.join("file '"+str(p)+"'" for p in scenes))
        filename='Ring-AIR-30s-Facebook.mp4' if social else 'Ring-AIR-30s-HD.mp4'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-i',str(OUT/'original-score.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-t','30','-movflags','+faststart',str(OUT/filename)],check=True)
    # Product cutdowns get the same original score, no licence dependency.
    for row in posts:
        if row['format']=='video':
            if row['slot']=='AM' and row['date']=='2026-10-04':
                row['filename']='Ring-AIR-30s-Facebook.mp4';continue
            src=OUT/row['filename'];tmp=OUT/(src.stem+'-sound.mp4')
            subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(src),'-i',str(OUT/'original-score.wav'),'-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(tmp)],check=True);tmp.replace(src)
    (OUT/'social-posts.json').write_text(json.dumps(posts,indent=2,ensure_ascii=False))
    with (OUT/'Youtopia-14-Day-Facebook-Plan.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(posts[0]));w.writeheader();w.writerows(posts)
    md=['# Youtopia Australia — 4–17 October 2026','', 'Two posts each day, 10:00 and 17:30 Australia/Sydney (AEDT, UTC+11 after the 4 October clock change). Product posts are drafts pending Ultrahuman approval. The website remains preview-only. No paid upgrades or ad spend.','', 'The commercial is a free motion-design edit of AI-assisted campaign artwork, not generated live-action footage. It includes original procedural music and exact titles.','', '| Date | 10:00 Ring AIR | Format | 17:30 Youtopia | Format |','|---|---|---|---|---|']
    for i in range(14):a,b=posts[i*2:i*2+2];md.append(f"| {a['date']} | {a['topic']} | {a['format']} | {b['topic']} | {b['format']} |")
    for row in posts:md+=['',f"## {row['date']} · {row['time']} · {row['topic']}",f"Media: {row['filename']} · {row['status']}",'',row['caption']]
    md+=['','## Sales growth actions','1. Use the fourteen different product questions to learn which creative earns genuine clicks and attributable sales. Track actual Awin orders and reversals; reach is not revenue.','2. Produce useful fit, cost and feature guides and searchable short videos. Publish the product guide only after preview and supplier approval.','3. Build an opt-in product newsletter with a useful wearable checklist; ask for subscriber permission and give an unsubscribe route. Do not send unsolicited bulk messages.','4. Seek authorised co-promotion with local coaches, wellness creators and community pages; do not post referral links on third-party properties without advertiser permission.','5. Present the approved creative and real click/conversion results to Ultrahuman; request campaign support, a permitted offer and confirmation of higher commission tiers. Current assigned rate is 7%; programme overview mentions 10%/15% revenue tiers but increases are not guaranteed or assumed.','6. iHerb next: Awin ROW 76736 advertises a 5% default and 7-day cookie, with limited up-to-25% campaigns. Application not submitted; confirm the actual assigned rate and terms before buying links.','7. Retain free organic promotion initially. No paid direct-link ads or Ultrahuman brand bidding without the advertiser’s written permission.','', 'Sources checked 3 October 2026: https://www.ultrahuman.com/au/ring/ ; https://www.ultrahuman.com/au/ring/faq/ ; signed-in Awin Commission Manager and programme terms for 69428 (24 September 2025); https://ui.awin.com/merchant-profile/76736 ; https://au.iherb.com/info/affiliates .']
    (OUT/'Youtopia-14-Day-Facebook-Plan.md').write_text('\n'.join(md))
    print(json.dumps({'output':str(OUT),'posts':len(posts),'film_duration':30}))

if __name__=='__main__':main()
