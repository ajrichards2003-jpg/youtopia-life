const CHANNELS = Object.freeze({
  youtopia: { id: '6ac242196a5c39ccb60f2f0a', name: 'Youtopia Life' },
  biohacker: { id: '6ac242196a5c39ccb60f2f0b', name: 'Biohacker Australia' },
});
const json = (body, status = 200) => new Response(JSON.stringify(body, null, 2), {
  status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
});
export default async (request) => {
  if (request.method !== 'POST') return json({ok:false,error:'POST required.'},405);
  let body;
  try { body = await request.json(); } catch { return json({ok:false,error:'Valid JSON required.'},400); }
  if (!body || typeof body !== 'object' || Array.isArray(body)) return json({ok:false,error:'Object body required.'},400);
  if (!Object.hasOwn(CHANNELS, body.channel)) return json({ok:false,error:'Channel is excluded from automation.'},403);
  const target = CHANNELS[body.channel];
  const text = typeof body.text === 'string' ? body.text.trim() : '';
  if (!text || text.length > 5000) return json({ok:false,error:'Post text must contain 1–5000 characters.'},400);
  // No implicit queue slot or immediate publication. Explicit UTC scheduling only.
  if (typeof body.dueAt !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$/.test(body.dueAt) || !Number.isFinite(Date.parse(body.dueAt)) || Date.parse(body.dueAt) <= Date.now()) {
    return json({ok:false,error:'A future ISO 8601 UTC dueAt is required.'},400);
  }
  const proposedInput = {text,channelId:target.id,schedulingType:'automatic',mode:'customScheduled',dueAt:new Date(body.dueAt).toISOString()};
  if (body.media) {
    let url;
    try { url = new URL(body.media.url); } catch { return json({ok:false,error:'Valid media URL required.'},400); }
    if (!['image','video'].includes(body.media.type) || url.protocol !== 'https:' || url.username || url.password || !['youtopialife.com','static.shareasale.com'].includes(url.hostname)) {
      return json({ok:false,error:'Use reviewed HTTPS campaign media.'},400);
    }
    proposedInput.assets = [{[body.media.type]:{url:url.href}}];
  }
  // This public endpoint always previews, including when confirm=true.
  // It never reads credentials, calls Buffer, or claims a post is approved/scheduled.
  return json({ok:true,executed:false,mode:'preview-only',target:target.name,proposedInput,message:'Nothing sent to Buffer. Production requires separate approval and a private executor.'});
};
