import test from 'node:test';
import assert from 'node:assert/strict';
import compose from '../netlify/functions/buffer-compose.mjs';
const dueAt = new Date(Date.now()+86400000).toISOString();
const send = (body) => compose(new Request('https://example.com/',{method:'POST',body:JSON.stringify(body)}));
test('two approved brands preview exact UTC slots without any network calls',async()=>{
 const oldFetch=global.fetch; global.fetch=()=>{throw Error('Unexpected external write');};
 try {for(const channel of ['youtopia','biohacker']){const r=await send({channel,text:'Reviewed post',dueAt,confirm:true});const p=await r.json();assert.equal(r.status,200);assert.equal(p.executed,false);assert.equal(p.mode,'preview-only');assert.equal(p.proposedInput.dueAt,dueAt);assert.equal(p.proposedInput.mode,'customScheduled');}}finally{global.fetch=oldFetch;}
});
test('Cardinia, arbitrary IDs, and prototype keys fail closed',async()=>{
 for(const channel of ['cardinia','6ac242196a5c39ccb60f2f0c','toString','__proto__','unknown'])assert.equal((await send({channel,text:'Test',dueAt})).status,403);
});
test('missing, local-time, invalid, and past slots cannot silently join queue',async()=>{
 for(const slot of [undefined,'2026-10-05T20:00:00','invalid','2020-01-01T00:00:00Z'])assert.equal((await send({channel:'youtopia',text:'Test',dueAt:slot})).status,400);
});
test('body shape, text and media validation',async()=>{
 for(const body of [null,[],{channel:'youtopia',text:'',dueAt},{channel:'youtopia',text:'Test',dueAt,media:{type:'image',url:'https://unreviewed.example/test.jpg'}}])assert.equal((await send(body)).status,400);
 const r=await send({channel:'youtopia',text:'Test',dueAt,media:{type:'image',url:'https://static.shareasale.com/image/149763/Ringlisting-03.jpg'}});assert.equal(r.status,200);assert.ok((await r.json()).proposedInput.assets[0].image);
});
