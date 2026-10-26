(()=>{
'use strict';
const get=id=>document.getElementById(id),duration=get('calm-duration'),start=get('calm-start'),pause=get('calm-pause'),reset=get('calm-reset'),cue=get('calm-cue'),count=get('calm-count'),progress=get('calm-progress'),orb=get('calm-orb');
let elapsed=0,last=0,running=false,timer=null,total=60,phase='';
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
function render(){const seconds=elapsed/1000,cycle=seconds%10,inhaling=cycle<5;const next=inhaling?'Breathe in gently':'Breathe out gently';if(running&&next!==phase){phase=next;cue.textContent=next}progress.value=seconds;count.textContent=`${Math.floor(seconds/10)} breathing cycles · ${Math.max(0,Math.ceil(total-seconds))} seconds remaining`;orb.style.transform=reduced.matches?'none':`scale(${1+(inhaling?cycle/5:(10-cycle)/5)*.45})`}
function tick(){if(!running)return;const now=performance.now();elapsed=Math.min(total*1000,elapsed+now-last);last=now;render();if(elapsed>=total*1000){halt();cue.textContent='Quest complete. A little moment of appreciation, earned.';start.disabled=false;start.textContent='Start again';duration.disabled=false}}
function halt(){running=false;clearInterval(timer);timer=null;pause.disabled=true;pause.textContent='Pause'}
function begin(){running=true;last=performance.now();pause.disabled=false;pause.textContent='Pause';start.disabled=true;duration.disabled=true;phase='';render();timer=setInterval(tick,100)}
function fresh(){halt();elapsed=0;total=Number(duration.value);progress.max=total;start.disabled=false;start.textContent='Start quest';duration.disabled=false;phase='';render();cue.textContent='Ready when you are.'}
start.addEventListener('click',()=>{fresh();begin()});pause.addEventListener('click',()=>{if(running){tick();if(!running)return;halt();pause.disabled=false;pause.textContent='Resume';cue.textContent='Paused. Breathe naturally.'}else begin()});reset.addEventListener('click',fresh);duration.addEventListener('change',fresh);document.addEventListener('visibilitychange',()=>{if(document.hidden&&running){tick();if(!running)return;halt();pause.disabled=false;pause.textContent='Resume';cue.textContent='Paused while away. Resume when ready.'}});fresh();
})();
