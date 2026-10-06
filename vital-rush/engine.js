/* Original Vital Rush simulation. No network, tracking or purchases. */
(function(root){
'use strict';
function seeded(seed){let s=seed>>>0;return()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
class Run{
 constructor({seed=Date.now(),gentle=false,practice=false}={}){this.random=seeded(seed);this.gentle=gentle;this.practice=practice;this.phase='running';this.lane=0;this.visualLane=0;this.jump=0;this.time=0;this.distance=0;this.points=0;this.food=0;this.energy=0;this.surge=0;this.shield=false;this.lives=3;this.invulnerable=0;this.objects=[];this.events=[];this.spawnClock=0.3;this.rows=0;}
 get score(){return Math.floor(this.distance*100)+this.points;}
 move(direction){if(this.phase==='running')this.lane=Math.max(-1,Math.min(1,this.lane+Math.sign(direction)));}
 leap(){if(this.phase==='running'&&this.jump===0)this.jump=.8;}
 pause(){if(this.phase==='running')this.phase='paused';}
 resume(){if(this.phase==='paused')this.phase='running';}
 finish(){this.phase='ended';}
 spawn(){if(this.practice&&this.rows<3){for(let lane=-1;lane<=1;lane++)this.objects.push({lane,z:1,kind:'food',food:this.rows%5,hit:false});this.rows++;return;}const blocked=Math.floor(this.random()*3)-1;const kind=this.rows<2?'hurdle':this.random()<.48?'hurdle':'wall';this.objects.push({lane:blocked,z:1,kind,hit:false});for(let lane=-1;lane<=1;lane++){if(lane===blocked)continue;const r=this.random();this.objects.push({lane,z:1,kind:r<.055?'shield':r<.13?'research':'food',food:Math.floor(this.random()*5),hit:false});}this.rows++;}
 tick(dt){if(this.phase!=='running')return;dt=Math.max(0,Math.min(dt,.05));this.time+=dt;this.jump=Math.max(0,this.jump-dt);this.surge=Math.max(0,this.surge-dt);this.invulnerable=Math.max(0,this.invulnerable-dt);const speed=(this.gentle?.18:.23)+Math.min(this.time/500,this.gentle?.09:.15);this.distance+=speed*dt;this.visualLane+=(this.lane-this.visualLane)*Math.min(1,dt*14);this.spawnClock-=dt;if(this.spawnClock<=0){this.spawn();this.spawnClock=this.gentle?1.75:1.45;}
 for(const o of this.objects){o.z-=speed*dt;if(o.z<=.08&&!o.hit){o.hit=true;if(o.lane!==this.lane)continue;if(o.kind==='food'){this.food++;this.energy+=10;this.points+=this.surge>0?100:50;this.events.push({kind:'food'});if(this.energy>=100){this.energy=0;this.surge=8;this.events.push({kind:'surge'});}}
 else if(o.kind==='research'){this.points+=this.surge>0?200:100;this.events.push({kind:'research'});}
 else if(o.kind==='shield'){this.shield=true;this.events.push({kind:'shield'});}
 else if(o.kind==='hurdle'&&Math.sin(this.jump/.8*Math.PI)>.4){this.points+=25;this.events.push({kind:'clear'});}
 else if(this.invulnerable===0){if(this.practice){this.invulnerable=1;this.events.push({kind:'practice-hit',obstacle:o.kind});}else if(this.surge>0){this.points+=25;this.events.push({kind:'clear'});}else if(this.shield){this.shield=false;this.invulnerable=1;this.events.push({kind:'saved'});}else{this.lives--;this.invulnerable=1.8;this.events.push({kind:'hit'});if(this.lives===0){this.finish();break;}}}}}
 this.objects=this.objects.filter(o=>o.z>-.2);if(this.practice&&this.time>=35)this.finish();
 }
 drain(){return this.events.splice(0);}
}
const api={Run,seeded};if(typeof module==='object'&&module.exports)module.exports=api;else root.VitalRushCore=api;
})(typeof globalThis==='object'?globalThis:this);
