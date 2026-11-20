import OpenAI from "openai";
import { getUser } from "@netlify/identity";
import { getStore } from "@netlify/blobs";

const DAILY_LIMIT = 3;
const MAX_BODY_BYTES = 2048;
const ALLOWED_ORIGINS = new Set(['https://youtopialife.com', 'https://www.youtopialife.com']);
const JSON_HEADERS = Object.freeze({
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store",
  "content-security-policy": "default-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
  "cross-origin-resource-policy": "same-origin",
  "referrer-policy": "no-referrer",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "x-robots-tag": "noindex, nofollow",
});
const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: JSON_HEADERS });

export default async (req) => {
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);
  const contentType = req.headers.get('content-type') || '';
  if (!/^application\/json(?:\s*;|$)/i.test(contentType)) return json({ error: 'JSON required' }, 415);
  const claimedLength = Number(req.headers.get('content-length'));
  if (Number.isFinite(claimedLength) && claimedLength > MAX_BODY_BYTES) return json({ error: 'Request too large' }, 413);
  const origin = req.headers.get('origin');
  if (origin && !ALLOWED_ORIGINS.has(origin) && !origin.endsWith('--playful-basbousa-781f5f.netlify.app')) return json({ error: 'Origin not allowed' }, 403);
  try {
    const user = await getUser();
    if (!user?.id) return json({ error: "Please sign in to Ask Youtopia." }, 401);

    const raw = await req.text();
    if (new TextEncoder().encode(raw).length > MAX_BODY_BYTES) return json({ error: 'Request too large' }, 413);
    let body;
    try { body = JSON.parse(raw); } catch { return json({ error: 'Invalid JSON' }, 400); }
    if (!body || typeof body !== 'object' || Array.isArray(body) || typeof body.question !== 'string') return json({ error: 'A question is required' }, 400);
    const question = body.question.trim();
    if (question.length > 600) return json({ error: 'Question must be 600 characters or fewer' }, 400);
    if (!question) return json({ error: "Ask a question first." }, 400);

    const day = new Date().toISOString().slice(0, 10);
    const key = `${user.id}/${day}`;
    const store = getStore({ name: "ask-youtopia-daily-usage", consistency: "strong" });
    const usage = (await store.get(key, { type: "json" })) || { used: 0 };
    if (usage.used >= DAILY_LIMIT) return json({ error: "Your three Youtopia wishes are used for today. The genie resets tomorrow (UTC). 🧞" }, 429);

    const client = new OpenAI();
    const response = await client.responses.create({
      model: "gpt-5.6-luna",
      input: [
        { role: "system", content: "You are Ask Youtopia, the evidence-aware discovery guide for Youtopia Life. Be concise, curious and useful. Distinguish established evidence, promising evidence, emerging research, anecdote and unresolved claims. Never treat a product claim as proof. Do not diagnose or prescribe. When relevant suggest what primary-source evidence the user should inspect and note uncertainty. Youtopia philosophy: curious enough to investigate, rigorous enough to question, independent enough to change our minds." },
        { role: "user", content: question }
      ],
      max_output_tokens: 500
    });
    const answer = response.output_text || "I couldn't produce an answer this time.";
    const used = usage.used + 1;
    await store.setJSON(key, { used, day });
    return json({ answer, remaining: DAILY_LIMIT - used });
  } catch (error) {
    console.error("Ask Youtopia request failed");
    return json({ error: "Ask Youtopia is temporarily unavailable. Please try again later." }, 503);
  }
};
// One canonical endpoint avoids bypassing the edge limit through the default function URL.
export const config = {
  path: "/api/ask-youtopia",
  rateLimit: { windowLimit: 20, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
